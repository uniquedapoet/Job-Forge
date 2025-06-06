import os
import pandas as pd
from openai import OpenAI
from models.resume import Resume
from services.resume_scraper import extract_text_from_pdf
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

def improve_bullets(user_id, job_posting_id=None):
    # Get user resume
    resume_file_name = Resume.get_resumes_by_user_id(user_id)

    if isinstance(resume_file_name, str):
        return {'error': resume_file_name}

    resume_file_name = resume_file_name['filename']
    RESUME_PATH = os.path.join("backend", "data", "resumes", resume_file_name)
    raw_resume = extract_text_from_pdf(RESUME_PATH)

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
    
    output_prompt = """\n
    **Output:**
    Provide raw json in this format: {string of the exact line that needs to be improved: string of the improved line}
    Please do not include quotes around the json.
    """

    jd_prompt = None
    if job_posting_id != None:
        # Get job description
        raw_job_description = get_job_desc(job_posting_id)

        jd_prompt = f"""
        Now, compare the resume to the following job description:
        
        **Job Description:**  
        {raw_job_description}  

        **Comparison Criteria:**
        1. **Skills Match**
        - Identify skills from the job description and check if they appear in the resume.
        - Highlight missing but relevant skills and suggest ways to incorporate them naturally.

        2. **Experience Alignment**
        - Compare required experience (years, industry, role-specific tasks) with the candidate’s background.
        - If experience does not fully match, suggest ways to highlight transferable skills.

        3. **Keywords & ATS Optimization**
        - Identify key industry-specific terms from the job description that should be included for ATS optimization.
        - Suggest where and how to integrate them into the resume.

        4. **Responsibilities & Achievements**
        - Check if the resume demonstrates achievements or responsibilities relevant to those in the job description.
        - Suggest rewording or restructuring if necessary to make it more aligned.

        5. **Education & Certifications**
        - Verify that required degrees, certifications, and qualifications from the job description are reflected in the resume.
        - If any are missing but the candidate has equivalent experience, suggest how to phrase it effectively.

        6. **Overall Resume Relevance Score**
        - Provide a score (out of 10) on how well the resume aligns with the job description.
        - Offer **three key improvements** that would make the resume stronger for this specific role.

        **Output:**
        Generate a structured comparison report with specific insights on how well the resume matches the job description, what improvements can be made, and how to increase the chances of passing ATS screening and catching the hiring manager’s attention.
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
