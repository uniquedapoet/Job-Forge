from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from database import validate_and_insert_resume
from flask_cors import CORS
import sqlite3
import os
from config import USER_DATABASE_URL
from database import create_users_table

# Initialize Flask app
app = Flask(__name__)

# Allow CORS for all routes
CORS(app, origins=["http://localhost:3000"])

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

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


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and (
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        )



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



if __name__ == "__main__":
    create_users_table()
    app.run(host="0.0.0.0", port=5001, debug=True)