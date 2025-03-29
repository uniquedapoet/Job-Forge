from config import JOBS_DATABASE_URL
from services.job_scraper import get_jobs_data
import time
from db_tools import state_abbreviations
from flask import Blueprint, jsonify, request
import sqlite3
import os
from models.jobs import Job, validate_and_insert_jobs


jobs = Blueprint("jobs", __name__)


@jobs.route("/", methods=["GET"])
def get_jobs():
    try:
        jobs = Job.jobs()

        return jsonify({"jobs": jobs}), 200

    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


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
        except Exception as e:
            # Log but don’t block search results
            print(f"Error inserting jobs: {str(e)}")

        if job_title and location:
            job_list = Job.jobs_by_location_and_title(
                location=location, title=job_title)

        elif job_title:
            job_list = Job.jobs_by_title(title=job_title)

        elif location:
            job_list = Job.jobs_by_location(location=location)

        return jsonify(
            {"message": "Jobs successfully retrieved!", "jobs": job_list}), 200

    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

