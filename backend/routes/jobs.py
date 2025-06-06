from services.job_scraper import get_jobs_data
from db_tools import state_abbreviations, clean_nans
from flask import Blueprint, jsonify, request
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
        jobs = get_jobs_data(job_title=job_title, location=location)

        if jobs is None:
            return jsonify({"error": "No matching jobs found"}), 404

        try:
            inserted_jobs = validate_and_insert_jobs(jobs)
        except Exception as e:
            print(f"Error inserting jobs: {str(e)}")

        if job_title and location:
            job_list = Job.jobs_by_location_and_title(
                location=location, title=job_title)

        elif job_title:
            job_list = Job.jobs_by_title(title=job_title)

        elif location:
            job_list = Job.jobs_by_location(location=location)

        job_list += inserted_jobs

        job_list = clean_nans(job_list)

        return jsonify(
            {"message": "Jobs successfully retrieved!", "jobs": job_list[:25]}), 200

    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@jobs.route('/<int:job_id>', methods=['GET'])
def get_job_by_id(job_id):
    try:
        job = Job.jobs_by_id(job_id)

        return jsonify({'jobs': job})

    except Exception as e:
        return jsonify({'error': f'Error Fetching Job data ({e})'})
