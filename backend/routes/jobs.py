# Scrapes job descriptions from URLs.
# Stores job applications in the database.

from resume import extract_text_from_pdf
from services.score import Score
import pandas as pd
import os

def get_score(user_id, job_posting_id, resume_path):
    try:
        # get job description from jobs csv using job_posting_id
        # TODO: create job_posting_id column in jobs csv
        file_path = os.path.join("backend", "data", "csvs", "jobs.csv")
        jobs = pd.read_csv(file_path)
        job_description = jobs.loc[jobs["job_posting_id"] == job_posting_id, "description"]

        # get score 
        raw_resume = extract_text_from_pdf(resume_path)
        score_obj = Score(raw_resume, job_description)
        similarity_score = score_obj.compute_similarity()

        return {
            "status": "success",
            "user_id": user_id,
            "job_posting_id": job_posting_id,
            "score": similarity_score,
            "message": "Similarity score computed successfully"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": "An error occurred while computing similarity score",
            "error": str(e)
        }
