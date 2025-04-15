from services.resume_scraper import extract_text_from_pdf
from services.score import Score
import os
from models.resume import Resume
from models.jobs import Job
from nltk.corpus import wordnet as wn


wn.ensure_loaded()


def get_score(user_id, job_posting_id):
    """Get the similarity score between a user's resume and a job posting."""
    from models.savedJobs import SavedJob

    try:
        # get job desctiption from jobs
        job_description = Job.description_by_id(job_posting_id)

        # get resume content with user id
        resume_file_name = Resume.get_resumes_by_user_id(user_id)
        
        if isinstance(resume_file_name, str):
            return {'error': resume_file_name}
        
        resume_file_name = resume_file_name['filename']
        RESUME_PATH = os.path.join("backend/data/resumes", resume_file_name)
        raw_resume = extract_text_from_pdf(RESUME_PATH)

        # get similarity score
        score_obj = Score(raw_resume, job_description)
        similarity_score = score_obj.compute_similarity() 

        score = similarity_score.item()
        # ===============================

        SavedJob.save_job_score(
            job_id=job_posting_id, user_id=user_id, job_score=score
            )

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