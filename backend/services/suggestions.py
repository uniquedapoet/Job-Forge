import os
import pandas as pd
from openai import OpenAI
from models.resume import Resume
from models.jobs import Job
from services.resume_scraper import extract_text_from_pdf
from dotenv import load_dotenv
import re
import json

load_dotenv(dotenv_path='backend/key.env')


def clean_key(key):
    # Keep letters, numbers, spaces, commas, and hyphens
    return re.sub(r'[^a-zA-Z0-9\s\-,]', '', key).strip()


def clean_json(json_string):
    # Remove markdown-style code block formatting
    if json_string.startswith("```json"):
        json_string = json_string[7:]  # Remove the opening ```json
    if json_string.endswith("```"):
        json_string = json_string[:-3]  # Remove the closing ```

    # Strip and remove newlines (optional depending on formatting)
    json_string = json_string.strip().replace('\n', '')

    # Now safely parse
    parsed_json = json.loads(json_string)

    # Handle if it's a list of dictionaries
    if isinstance(parsed_json, list):
        return [
            {clean_key(k): v.strip() if isinstance(v, str) else v for k, v in item.items()}
            for item in parsed_json if isinstance(item, dict)
        ]

    elif isinstance(parsed_json, dict):
        return {clean_key(k): v.strip() if isinstance(v, str) else v for k, v in parsed_json.items()}

    else:
        raise ValueError("Parsed JSON is neither a dictionary nor a list of dictionaries.")


def general_suggestions(resume_text):
    # Get user resume
    raw_resume = resume_text

    base_prompt = f"""
    You are an expert in career development and resume optimization, specializing in crafting resumes that maximize job application success. 
    I will provide you with resume and you will analyze the bullet points (lines begining with "-") and provide improvments while not making 
    up statistics, if you beleive adding statistics will improve the bullet us X as a filler for any quantitative metric.
    Please provide an improved bullet point for each bullet point marked with "-".
    
    **Users Resume**:
    {raw_resume}

    **Experience Evaluation Principles**
    - Verify the presence of job title, company name, location, and dates of employment.
    - Ensure key responsibilities and achievements are quantifiable, action-driven, and aligned with industry standards.
    - Apply the following best practices:
        - **Use numbers:** Quantify actions whenever possible (e.g., "organized 10+ events," "served 50+ clients," "increased sales by 25%").
        - **Focus on outcomes:** Highlight the end result or impact of the work. Did the candidate improve a process? Increase engagement? Save time or money?
        - **Be specific about contributions:** Instead of general statements, specify what exactly was done and how it added value to the team, project, or company.
        - **Use strong action verbs:** Ensure bullet points begin with dynamic verbs from the following list:

        Achieved, Accomplished, Advised, Analyzed, Applied, Arranged, Assembled, Built, Championed, Coordinated, Delivered, Designed, Developed, 
        Directed, Enhanced, Established, Facilitated, Formulated, Generated, Implemented, Improved, Increased, Influenced, Initiated, Led, 
        Monitored, Oversaw, Planned, Produced, Resolved, Streamlined, Supervised, Trained, Upgraded, Utilized, Validated, Verified, Directed, 
        Launched, Executed, Negotiated, Optimized, Researched, Revised, Tested, Supported, Transformed.

    
    **Projects Evaluation Principles**
    - Evaluate clarity in describing role, technologies used, and project outcomes.
    - Suggest how to make descriptions more results-oriented.
    """

    output_prompt = """
    **Output Instructions (IMPORTANT):**

    Return only valid raw JSON in the following format:

    {
      "ImprovedBullets": [
        {
          "original": "Original bullet point text here.",
          "improved": "Improved version of the bullet point here."
        },
        ...
      ],
      "GeneralSuggestions": [
        "General improvement suggestion 1",
        "General improvement suggestion 2",
        ...
      ]
    }

    ⚠️ Do not include any extra text, markdown, comments, or explanation outside the JSON.
    ⚠️ Ensure all keys and values are wrapped in double quotes ( " " ).
    ⚠️ Do not use single quotes ( ' ), curly quote characters, or smart quotes.
    ⚠️ Escape all inner double quotes inside string values.
    ⚠️ Make sure the entire response is valid JSON that can be parsed by json.loads().
    """

    prompt = base_prompt + output_prompt
    API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=API_KEY)

    # Request GPT-4o
    response = client.chat.completions.create(
        model="gpt-4o",  # Updated model name
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )

    response = response.choices[0].message.content
    response_json = clean_json(response)

    return response_json


def job_based_suggestions(user_id, job_id):
    # Get user resume
    resume = Resume.get_resumes_by_user_id(user_id)
    raw_resume = resume['resume_text']

    # Get job description
    raw_job_description = Job.description_by_id(job_id)

    base_prompt = f"""
    You are an expert in resume optimization and job targeting for maximum application success.

    I will provide:
    - A user's current resume (including bullet points marked with "-"),
    - A job posting (with responsibilities, qualifications, and listed technologies/skills).

    Your tasks:
    1. Analyze the resume and the job posting.
    2. Identify specific technologies from the job posting that are missing or underrepresented on the resume and that should be added.
    3. Identify specific soft skills from the job posting that should naturally be incorporated into the resume if possible.
    4. Identify specific certifications, frameworks, or methodologies from the job posting that would strengthen the resume.
    5. Identify easy-to-add keywords or phrases from the job posting that match its language and could quickly strengthen the resume.
    6. Tailor all recommendations based strictly on the job description, avoiding general advice.

    **User's Resume:**
    {raw_resume}

    **Job Description:**
    {raw_job_description}

    ⚠️ Important Rules:
    - ONLY use double quotes ( " " ) throughout the JSON.
    - Escape any inner double quotes if needed.
    - Do NOT rewrite or edit the resume bullet points.
    - Do NOT add extra commentary, markdown, or headings.
    - Output must be fully valid JSON that can be parsed with json.loads().

    **Output Format:**
    Return only a JSON object structured exactly like this:

    {{
      "JobBasedSuggestions": {{
        "TechnologiesToAdd": ["List specific technologies pulled from the job post"],
        "SoftSkillsToAdd": ["List specific soft skills pulled from the job post"],
        "CertificationsOrFrameworksToAdd": ["List specific certifications, frameworks, or methodologies pulled from the job post"],
        "EasyKeywordWins": ["Other quick keywords/phrases aligned with the job post that could be added easily"]
      }}
    }}
    """

    API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=API_KEY)

    # Request GPT-4o
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": base_prompt}],
        stream=False
    )

    response = response.choices[0].message.content
    response_json = clean_json(response)

    return response_json
