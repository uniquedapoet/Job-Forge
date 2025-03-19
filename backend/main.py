from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from routes.resume import validate_and_insert_resume, allowed_file
from flask_cors import CORS
import sqlite3
import os
from config import USER_DATABASE_URL, JOBS_DATABASE_URL
from services.job_scraper import get_jobs_data
from routes.jobs import validate_and_insert_jobs, create_jobs_db
import time
from services.resume_scorer import get_score
from services.sections_suggestions import improve_sections
from db_tools import correct_spelling, state_abbreviations
from routes.users import create_saved_jobs_table, get_job_score, save_job_data


# Initialize Flask app
app = Flask(__name__)
os.environ['TOKENIZERS_PARALLELISM'] = "false"
# Allow CORS for all routes
CORS(app, origins=["http://localhost:3000"])


@app.route("/", methods=["GET"])
def read_root():
    return jsonify({"message": "Backend is running"})


@app.route("/users", methods=["GET"])
def get_users():
    conn = sqlite3.connect(USER_DATABASE_URL)
    cursor = conn.cursor()

    # Fetch all users
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    # Get column names
    column_names = [description[0] for description in cursor.description]

    # Convert tuples to list of dictionaries
    user_list = [dict(zip(column_names, user)) for user in users]

    conn.close()

    return jsonify({"users": user_list})


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = sqlite3.connect(USER_DATABASE_URL)
    cursor = conn.cursor()

    # Fetch user by ID
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    # Get column names
    column_names = [description[0] for description in cursor.description]

    conn.close()

    if user:
        return jsonify({"user": dict(zip(column_names, user))})
    else:
        return jsonify({"error": "User not found"}), 404


@app.route("/register_user", methods=["POST"])
def register_user():
    conn = sqlite3.connect(USER_DATABASE_URL)
    cursor = conn.cursor()

    user_data = request.json

    try:
        cursor.execute("""
        INSERT INTO users (username, email, password, first_name, last_name, phone, city, zipcode, job_titles)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_data["username"],
            user_data["email"],
            user_data["password"],  # Should be hashed before storing
            user_data["first_name"],
            user_data["last_name"],
            user_data.get("phone"),
            user_data.get("city"),
            user_data.get("zipcode"),
            user_data.get("job_titles"),
        ))

        conn.commit()
        return jsonify({"message": "User created successfully"}), 201

    except sqlite3.IntegrityError as e:
        return jsonify({"error": f"Error inserting user {user_data['username']}: {e}"}), 400

    finally:
        conn.close()


@app.route("/upload", methods=["POST"])
def upload_resume():
    """Upload a resume file to the server. and store it. Called with file """
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    user_id = request.form.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    if file and allowed_file(file.filename):
        validate_and_insert_resume(user_id, file)
        return jsonify({"message": "File uploaded successfully"}), 201

    return jsonify({"error": "File type not allowed"}), 400


@app.route("/download/<filename>", methods=["GET"])
def download_resume(filename):
    """Flask endpoint to serve a stored resume."""
    file_path = os.path.join('data/resumes', secure_filename(filename))

    if os.path.exists(file_path):
        return send_from_directory('data/resumes', filename, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404


@app.route("/job_search", methods=["POST"])
def job_search():
    request_data = request.json
    job_title = request_data.get("job_title", "").strip()
    location = request_data.get("location", "").strip()

    job_title = correct_spelling(job_title)
    location = state_abbreviations(location)

    if not job_title and not location:
        return jsonify({"error": "At least one search criteria is required"}), 400

    try:
        # Fetch jobs based on the search criteria
        jobs = get_jobs_data(job_title=job_title, location=location)

        if jobs is None:
            return jsonify({"error": "No matching jobs found"}), 404

        # Try inserting jobs into the database
        try:
            validate_and_insert_jobs(jobs)
            time.sleep(1)  # Wait 1 second before querying
        except Exception as e:
            # Log but don’t block search results
            print(f"Error inserting jobs: {str(e)}")

        # Query the database to get relevant jobs
        conn = sqlite3.connect(JOBS_DATABASE_URL)
        cursor = conn.cursor()

        # Build dynamic query for filtering
        query = "SELECT * FROM jobs WHERE 1=1"
        params = []

        if job_title:
            words = job_title.split()  # Split the search term into individual words
            # Create conditions dynamically
            conditions = " OR ".join(["title LIKE ?"] * len(words))
            query += f" AND ({conditions})"  # Add to the existing query
            # Append parameters for each word
            params.extend([f"%{word}%" for word in words])

        if location:
            query += " AND location LIKE ?"
            params.append(f"%{location}%")  # Allow partial matching

        print(f"Params: {params}")
        cursor.execute(query, params)
        jobs = cursor.fetchall()

        # Get column names
        column_names = [description[0] for description in cursor.description]

        # Convert tuples to list of dictionaries
        job_list = [dict(zip(column_names, job)) for job in jobs]

        conn.close()

        if not job_list:
            return jsonify({"error": "No matching job list found"}), 404

        return jsonify({"message": "Jobs successfully retrieved!", "jobs": job_list}), 200

    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route("/jobs", methods=["GET"])
def get_jobs():
    if not os.path.exists(JOBS_DATABASE_URL):
        create_jobs_db()

    conn = sqlite3.connect(JOBS_DATABASE_URL)
    cursor = conn.cursor()

    # Fetch all jobs
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()

    # Get column names
    column_names = [description[0] for description in cursor.description]

    # Convert tuples to list of dictionaries
    job_list = [dict(zip(column_names, job)) for job in jobs]

    return jsonify({"jobs": job_list})


@app.route("/resume_score", methods=["POST"])
def resume_score():
    request_data = request.json
    user_id = request_data.get("user_id")
    job_posting_id = request_data.get("job_posting_id")
    print(f"User ID: {user_id}, Job Posting ID: {job_posting_id}")

    if not user_id or not job_posting_id:
        return jsonify({"error": "User ID and job posting ID are required"}), 400

    job_score = get_job_score(user_id, job_posting_id)
    print(f"Job score: {job_score}")

    if not job_score:
        try:
            job_score = get_score(user_id, job_posting_id)

        except Exception as e:
            return jsonify({"error": f"Error computing similarity score: {str(e)}"}), 500

    # return jsonify({"score": job_score, "status": "success"}), 200
    return jsonify(job_score), 200


@app.route("/resume/suggestions", methods=["POST"])
def get_resume_suggestions():
    user_id = request.json.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    try:
        suggestions = improve_sections(user_id)
        return jsonify({"success": True, "suggestions": suggestions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
