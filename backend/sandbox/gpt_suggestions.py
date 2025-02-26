import os
import pandas as pd
from openai import OpenAI
import db_tools
from services.resume_scraper import extract_text_from_pdf

def get_suggestions(user_id, job_posting_id):
    """Get suggestion from OpenAI API gpt-4o for the users resume given a job description."""

    # Get user resume
    resume_file_name = db_tools.get_resumes_by_user_id(user_id)[0]['filename']
    RESUME_PATH = os.path.join("data", "resumes", resume_file_name)
    raw_resume = extract_text_from_pdf(RESUME_PATH)

    # Get job description
    JOBS_PATH = os.path.join("data", "csvs", "jobs.csv")
    jobs = pd.read_csv(JOBS_PATH)
    raw_job_description = jobs.loc[jobs["job_id"] == job_posting_id, "description"].iloc[0]

 
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

    Please return the response in a json structured format applicable to an api with sections for:
    - skills_to_develop
    - keywords
    - grammar_formatting
    """

    #TODO: Figure out away to make the key universal for users, 
    # maybe have users input their own api key
    API_KEY = os.getenv("OPEN_API_KEY")  
    client = OpenAI(api_key=API_KEY) 

    # Request GPT-4o
    response = client.chat.completions.create(
        model="gpt-4o",  # Updated model name
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )

    return response.choices[0].message.content
