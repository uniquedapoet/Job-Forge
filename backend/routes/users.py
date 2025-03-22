from flask import Blueprint, jsonify, request
from models.users import User
from models.savedJobs import SavedJob

users = Blueprint("users", __name__)


@users.route("/", methods=["GET"])
def get_users():
    User.create_tables()
    users = User.users()

    if not users:
        User.from_csv("data/csvs/user_data.csv")
        users = User.users()

    user_list = [{column.key: getattr(
        user, column.key) for column in User.__table__.columns} for user in users]

    return jsonify({"users": user_list})


@users.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.user(user_id)

    if user:
        return jsonify({"user": user})
    else:
        return jsonify({"error": "User not found"}), 404


@users.route("/register_user", methods=["POST"])
def register_user():
    user_data = request.json

    if not user_data:
        return jsonify({"error": "No user data provided"}), 400

    try:
        User.register(user_data)
        return jsonify({"message": "User created successfully"}), 201

    except Exception as e:
        return jsonify({"error": f"Error creating user: {str(e)}"}), 400


@users.route("/<int:user_id>/saved_jobs", methods=["GET"])
def get_saved_jobs(user_id):
    saved_jobs = SavedJob.get_saved_jobs(user_id)

    if saved_jobs:
        return jsonify(saved_jobs)
    else:
        return jsonify({"error": "No saved jobs found"}), 404   
