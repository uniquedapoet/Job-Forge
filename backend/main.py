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
from routes.users import User, SavedJob


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
    User.create_tables()
    users = User.users()

    if not users:
        User.from_csv("data/csvs/user_data.csv")
        users = User.users()
    
    user_list = [{column.key: getattr(user, column.key) for column in User.__table__.columns} for user in users]

    return jsonify({"users": user_list})


# change to new user model
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.user(user_id)

    user = {
        column.key: getattr(user, column.key) 
        for column in User.__table__.columns
        }
    
    if user:
        return jsonify({"user": user})
    else:
        return jsonify({"error": "User not found"}), 404


@app.route("/register_user", methods=["POST"])
def register_user():
    user_data = request.json

    if not user_data:
        return jsonify({"error": "No user data provided"}), 400

    try:
        User.register(user_data)
        return jsonify({"message": "User created successfully"}), 201

    except Exception as e:
        return jsonify({"error": f"Error creating user: {str(e)}"}), 400  


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


# PROBLEM: IF NEW RESUME IS UPLOADED, THE SCORE IS NOT UPDATED IF IT WAS ALREADY CALCULATED
@app.route("/resume_score", methods=["POST"])
def resume_score():
    request_data = request.json
    user_id = request_data.get("user_id")
    job_posting_id = request_data.get("job_posting_id")
    print(f"User ID: {user_id}, Job Posting ID: {job_posting_id}")

    if not user_id or not job_posting_id:
        return jsonify({"error": "User ID and job posting ID are required"}), 400

    job_score = SavedJob.get_job_score(user_id, job_posting_id)
    print(f"Job score: {job_score}")

    if not job_score:
        try:
            job_score = get_score(user_id, job_posting_id).score

        except Exception as e:
            return jsonify({"error": f"Error computing similarity score: {str(e)}"}), 500


    return jsonify(round((job_score*100), 2)), 200


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
