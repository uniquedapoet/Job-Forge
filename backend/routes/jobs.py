from config import JOBS_DATABASE_URL
from services.job_scraper import get_jobs_data
from models.jobs import validate_and_insert_jobs, create_jobs_db
import time
from db_tools import state_abbreviations
from flask import Blueprint, jsonify, request
import sqlite3
import os

jobs = Blueprint("jobs", __name__)


@jobs.route("/", methods=["GET"])
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


@jobs.route("/job_search", methods=["POST"])
def job_search():
    request_data = request.json
    job_title = request_data.get("job_title", "").strip()
    location = request_data.get("location", "").strip()

    location = state_abbreviations(location)

    if not job_title and not location:
        return jsonify(
            {"error": "At least one search criteria is required"}), 400

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
            words = job_title.split()

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

        return jsonify(
            {"message": "Jobs successfully retrieved!", "jobs": job_list}), 200

    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
