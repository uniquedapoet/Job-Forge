from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
from config import USER_DATABASE_URL

from database import create_users_table, test_user_data

# Initialize Flask app
app = Flask(__name__)

# Allow CORS for all routes
CORS(app)  # Apply CORS to the entire app without specific restrictions


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


if __name__ == "__main__":
    create_users_table()
    app.run(host="0.0.0.0", port=5001, debug=True)