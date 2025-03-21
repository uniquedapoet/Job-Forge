import os
from openai import OpenAI
from db_tools import get_resumes_by_user_id, get_job_desc
from services.resume_scraper import extract_text_from_pdf

def get_suggestions(user_id, job_posting_id=None):
    """Get suggestion from OpenAI API gpt-4o for the users resume or the users resume given a job description."""

    # Get user resume
    resume_file_name = get_resumes_by_user_id(user_id)[0]['filename']
    RESUME_PATH = os.path.join("data", "resumes", resume_file_name)
    raw_resume = extract_text_from_pdf(RESUME_PATH)

    base_prompt = f"""
    You are an expert in career development and resume optimization, specializing in crafting resumes that maximize job application success. 
    I will provide you with a resume. Your task is to critically evaluate its content and structure, following these principles.

    **Resume:** 
    {raw_resume}

    **Evaluation Principles:**

    1. **Contact Information**
    - Ensure name, phone number, email, and LinkedIn profile/professional website are present and correctly formatted.
    - Check for professionalism in email and consistency in formatting.

    2. **Executive Summary**
    - Assess clarity, conciseness, and relevance to the target job/industry.
    - Suggest improvements to make it more impactful and tailored.

    3. **Work Experience**
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

    - Suggest rewording where necessary to enhance clarity and impact.

    4. **Education**
    - Check for completeness: degree(s), institution names, and graduation dates.
    - Identify if relevant coursework or honors would strengthen the resume.

    5. **Skills**
    - Ensure a balanced mix of technical and professional skills.
    - Recommend any industry-specific or in-demand skills that may be missing.

    6. **Certifications and Licenses**
    - Verify relevance and completeness. Suggest additional certifications if applicable.

    7. **Achievements and Awards**
    - Ensure all notable recognitions are included and well-articulated.

    8. **Projects**
    - Evaluate clarity in describing role, technologies used, and project outcomes.
    - Suggest how to make descriptions more results-oriented.

    9. **Affiliations/Community Involvement**
    - Ensure relevant memberships, leadership roles, and contributions are effectively highlighted.

    10. **Overall Formatting & Readability**
    - Assess whether the resume is well-structured, concise, and easy to scan.
    - Identify any issues with layout, font choices, bullet points, or section ordering.

    **Output:**
    Provide a structured evaluation with specific feedback for each section. 
    Include clear recommendations for improvement, examples of better wording if necessary, and suggestions to enhance impact and clarity. 
    If anything is missing, highlight it and explain why adding it would strengthen the resume.
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

    #TODO: Figure out away to make the key universal for users, 
    # maybe have users input their own api key
    API_KEY = os.getenv("OPENAI_API_KEY")  
    client = OpenAI(api_key=API_KEY) 

    # Get final prompt
    if jd_prompt != None:
        prompt = base_prompt + "\n\n" + jd_prompt
    prompt = base_prompt

    # Request GPT-4o
    response = client.chat.completions.create(
        model="gpt-4o",  # Updated model name
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )

    return response.choices[0].message.content
