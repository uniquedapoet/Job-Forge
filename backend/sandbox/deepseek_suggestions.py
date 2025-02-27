import os
import sys
import pandas as pd
from openai import OpenAI
# import db_tools
from backend.services.resume_scraper import extract_text_from_pdf


def get_suggestions(user_id, job_posting_id):

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(backend_dir, "data")

    API_KEY = os.getenv("deepseek")
    client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

    db_tools.get_resumes_by_user_id(user_id)
    resume_data = db_tools.get_resumes_by_user_id(user_id)
    resume_file_name = resume_data[0]['filename']
    RESUME_PATH = os.path.join(data_dir, "resumes", resume_file_name)
    raw_resume = extract_text_from_pdf(RESUME_PATH)

    JOBS_PATH = os.path.join(data_dir, "csvs", "jobs.csv")
    jobs = pd.read_csv(JOBS_PATH)
    raw_job_description = jobs.loc[jobs["job_id"] == job_posting_id, "description"][0]


# use the keyword analysis that was used fo the door dash jobs in protfolio class


    # Format the prompt
    prompt = f"""
    You are an expert resume advisor. Your task is to provide actionable, realistic suggestions to optimize a user's resume for a specific job description. 
    Focus on:
    1. Relevant skills to highlight or develop that are within reach for the user.
    2. Keywords to include that match the job description and industry.
    3. Grammar and phrasing improvements to sound more professional and clear.
    4. Avoid suggesting unattainable skills or unrealistic qualifications.
    5. Provide concise, practical recommendations that the user can implement quickly.

    User's Resume:
    {raw_resume}

    Job Description:
    {raw_job_description}

    Please return the response in a structured format with sections for:
    - Skills to Develop
    - Keywords to Include
    - Grammar & Formatting Suggestions
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )

    return response.choices[0].message.content