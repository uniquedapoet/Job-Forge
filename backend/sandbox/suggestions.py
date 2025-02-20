import os
from openai import OpenAI


def get_suggestions(user_id, resume_path, job_description_id):
    API_KEY = os.getenv("deepseek")
    client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

    # get resume content

    # get job description_content

    # Format the prompt
    prompt = """
    You are an expert resume advisor. Your task is to provide actionable, realistic suggestions to optimize a user's resume for a specific job description. 
    Focus on:
    1. Relevant skills to highlight or develop that are within reach for the user.
    2. Keywords to include that match the job description and industry.
    3. Grammar and phrasing improvements to sound more professional and clear.
    4. Avoid suggesting unattainable skills or unrealistic qualifications.
    5. Provide concise, practical recommendations that the user can implement quickly.

    User's Resume:
    {resume_content}

    Job Description:
    {job_description_content}

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