from services.resume_scraper import extract_text_from_pdf
from services.score import Score
import pandas as pd
import db_tools
import os


def get_score(user_id, job_posting_id):
    """Get the similarity score between a user's resume and a job posting."""
    try:
        # get job desctiption from jobs csv
        JOBS_PATH = 'backend/data/csvs/jobs.csv'
        jobs = pd.read_csv(JOBS_PATH)
        job_description = jobs.loc[jobs["job_id"] == job_posting_id, "description"].iloc[0]

        # get resume content with user id
        resume_file_name = db_tools.get_resumes_by_user_id(user_id)[0]['filename']
        RESUME_PATH = os.path.join('backend',"data", "resumes", resume_file_name)
        raw_resume = extract_text_from_pdf(RESUME_PATH)

        # get similarity score
        score_obj = Score(raw_resume, job_description)
        similarity_score = score_obj.compute_similarity() 
        score = f"{round(similarity_score.item(),2)*100}%" # get percentage score from the tensor
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
    