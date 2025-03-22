from services.resume_scraper import extract_text_from_pdf
from services.score import Score
from db_tools import get_job_desc, get_resumes_by_user_id
import os
from models.savedJobs import SavedJob
from nltk.corpus import wordnet as wn


wn.ensure_loaded()


def get_score(user_id, job_posting_id):
    """Get the similarity score between a user's resume and a job posting."""
    try:
        # get job desctiption from jobs
        job_description = get_job_desc(job_posting_id)

        # get resume content with user id
        resume_file_name = get_resumes_by_user_id(user_id)[0]['filename']
        RESUME_PATH = os.path.join("backend/data/resumes", resume_file_name)
        raw_resume = extract_text_from_pdf(RESUME_PATH)

        # get similarity score
        score_obj = Score(raw_resume, job_description)
        similarity_score = score_obj.compute_similarity() 

        score = similarity_score.item()
        # ===============================

        saved_job = SavedJob(user_id=user_id, job_id=job_posting_id, job_score=score)
        saved_job.save()

        print(f"Similarity score between user {user_id}'s resume and job posting {job_posting_id}: {score}")
        return {
                "status": "success",
                "user_id": user_id,
                "job_posting_id": job_posting_id,
                "score": score,
                "message": "Similarity score computed successfully"
            }
        
    except Exception as e:
        return {
            "status": "error",
            "message": "An error occurred while computing similarity score",
            "error": str(e)
        }