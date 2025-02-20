from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from routes.resume import validate_and_insert_resume, allowed_file
from flask_cors import CORS
import sqlite3
import os
from config import USER_DATABASE_URL, JOBS_DATABASE_URL
from routes.auth import test_get_score

# Initialize Flask app
app = Flask(__name__)

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


@app.route("/jobs", methods=["GET"])
def get_jobs():
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
    

if __name__ == "__main__":
    test_get_score()
    # app.run(host="0.0.0.0", port=5001, debug=True)