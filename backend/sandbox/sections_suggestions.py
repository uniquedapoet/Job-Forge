import os
import pandas as pd
from openai import OpenAI
import db_tools
from services import resume_scraper as rs
import re
import json

def clean_json(json_string):
    """
    Cleans a JSON string by:
    - Removing problematic characters from keys (e.g., «, », special symbols)
    - Stripping leading and trailing spaces from both keys and values
    """
    def clean_key(key):
        key = re.sub(r'[^a-zA-Z0-9\s\-,]', '', key)  # Keep letters, numbers, spaces, commas, and hyphens
        return key.strip()

    # Load JSON safely
    parsed_json = json.loads(json_string)

    # Clean keys and strip values
    cleaned_json = {clean_key(key): value.strip() for key, value in parsed_json.items()}

    return cleaned_json

def improve_sections(user_id):
    # Get user resume
    resume_file_name = db_tools.get_resumes_by_user_id(user_id)[0]['filename']
    RESUME_PATH = os.path.join("data", "resumes", resume_file_name)
    raw_resume = rs.extract_text_from_pdf(RESUME_PATH)
    sections = rs.extract_resume_sections(raw_resume)

    base_prompt = f"""
    You are an expert in career development and resume optimization, specializing in crafting resumes that maximize job application success. 
    I will provide you with resume sections: education, experience, and projects. Your task is to evalute the content based on these principles:

    **Users Resume Experience Section**:
    {sections['Experience']}

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

    **Users Resume Education Section**:
    {sections['Education']}

    **Education Evaluation Principles**
    - Check for completeness: degree(s), institution names, and graduation dates.
    - Identify if relevant coursework or honors would strengthen the resume.

    **Users Resume Projects Section**:
    {sections['Projects']}

    **Projects Evaluation Principles**
    - Evaluate clarity in describing role, technologies used, and project outcomes.
    - Suggest how to make descriptions more results-oriented.
    """ 
    
    output_prompt = """\n
    **Output:**
    Provide raw json in this format: {string of the exact line that needs to be improved: string of the improved line}
    Please do not include quotes around the json.
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