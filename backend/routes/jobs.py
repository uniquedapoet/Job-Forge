# Scrapes job descriptions from URLs.
# Stores job applications in the database.
import sys
import os

# Append the backend directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from resume import extract_text_from_pdf
from services.score import Score
import pandas as pd
import db_tools

script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(script_dir)
data_dir = os.path.join(backend_dir, "data")
JOBS_PATH = os.path.join(data_dir, "csvs", "jobs.csv")


def get_score(user_id, job_posting_id):
    # try:
        # get job description from jobs csv using job_posting_id
        # TODO: create job_posting_id column in jobs csv

    jobs = pd.read_csv(JOBS_PATH)
    job_description = jobs.loc[jobs["id"] == job_posting_id, "description"][0]

    resume_data = db_tools.get_resumes_by_user_id(user_id)
    resume_file_name = resume_data[0]['filename']
    RESUME_PATH = os.path.join(data_dir, "resumes", resume_file_name)
    raw_resume = extract_text_from_pdf(RESUME_PATH)

    score_obj = Score(raw_resume, job_description)
    similarity_score = score_obj.compute_similarity()
    return similarity_score

    #     return {
    #         "status": "success",
    #         "user_id": user_id,
    #         "job_posting_id": job_posting_id,
    #         "score": similarity_score,
    #         "message": "Similarity score computed successfully"
    #     }
    
    # except Exception as e:
    #     return {
    #         "status": "error",
    #         "message": "An error occurred while computing similarity score",
    #         "error": str(e)
    #     }
    
if __name__ == "__main__":
    print(get_score(1,"in-b26a372f08fef696"))

