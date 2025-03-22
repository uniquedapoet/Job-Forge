from models.resume import Resume
from models.savedJobs import SavedJob
from flask import Blueprint, jsonify, request
from services.sections_suggestions import improve_sections
from services.resume_scorer import get_score


resumes = Blueprint("resumes", __name__)


@resumes.route("/upload", methods=["POST"])
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

    if file and Resume.allowed_file(file.filename):
        Resume.insert_resume(user_id, file)
        return jsonify({"message": "File uploaded successfully"}), 201

    return jsonify({"error": "File type not allowed"}), 400


#  PROBLEM: IF NEW RESUME IS UPLOADED, THE SCORE IS NOT UPDATED IF IT WAS ALREADY CALCULATED
@resumes.route("/resume_score", methods=["POST"])
def resume_score():
    request_data = request.json
    user_id = request_data.get("user_id")
    job_posting_id = request_data.get("job_posting_id")
    print(f"User ID: {user_id}, Job Posting ID: {job_posting_id}")

    if not user_id or not job_posting_id:
        return jsonify({"error": "User ID and job posting ID are required"}), 400
    
    try:
        job_score = SavedJob.get_job_score(user_id, job_posting_id)
        job_score = None if job_score == 0 else job_score

    except Exception:
        if not job_score:
            try:

                job_score = get_score(user_id, job_posting_id)
                if isinstance(job_score, dict):
                    job_score = job_score['score']
                    
                print(f"Job score: {job_score}")
            except Exception as e:
                return jsonify({"error": f"Error computing similarity score: {str(e)} {job_score}"}), 500

    return jsonify({"score":round((job_score*100), 2)}), 200


@resumes.route("/resumes/suggestions", methods=["POST"])
def get_resume_suggestions():
    user_id = request.json.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    try:
        suggestions = improve_sections(user_id)
        return jsonify({"success": True, "suggestions": suggestions})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

