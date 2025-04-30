from services.score import Score
from models.resume import Resume
from models.jobs import Job
from nltk.corpus import wordnet as wn  # type: ignore


wn.ensure_loaded()


def similarity_to_score(similarity):
    if similarity < 0.05:
        return 1
    elif similarity < 0.1:
        return 2
    elif similarity < 0.2:
        return 4
    elif similarity < 0.5:
        return 6
    elif similarity < 0.6:
        return 7
    elif similarity < 0.75:
        return 8
    elif similarity < 0.9:
        return 9
    else:
        return 10


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

        score = similarity_to_score(similarity_score.item())

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