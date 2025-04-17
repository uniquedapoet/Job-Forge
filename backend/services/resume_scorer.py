from services.score import Score
from models.resume import Resume
from models.jobs import Job
from nltk.corpus import wordnet as wn  # type: ignore


wn.ensure_loaded()


def get_score(user_id, job_posting_id):
    """Get the similarity score between a user's resume and a job posting."""
    from models.savedJobs import SavedJob

    try:
        # get job desctiption from jobs
        job_description = Job.description_by_id(job_posting_id)

        raw_resume = Resume.get_resume_text(user_id)

        # get similarity score
        score_obj = Score(raw_resume, job_description)
        similarity_score = score_obj.compute_similarity()

        score = similarity_score.item()
        # ===============================

        SavedJob.save_job_score(
            job_id=job_posting_id, user_id=user_id, job_score=score
        )
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
