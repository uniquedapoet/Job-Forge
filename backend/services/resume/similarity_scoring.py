import re
import spacy
from sentence_transformers import SentenceTransformer
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

def clean_text(raw_text):
    set_of_stopwords = set(stopwords.words("english") + list(string.punctuation))
    lemmatizer = WordNetLemmatizer()

    # Convert text to lowercase and tokenize into words
    tokens = word_tokenize(raw_text.lower())
    # Remove stopwords and punctuation
    tokens = [token for token in tokens if token not in set_of_stopwords]
    # Lemmatize the remaining words
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    # Join the tokens back into a single string
    cleaned_text = " ".join(tokens)
    return cleaned_text

def clean_resume(resume_content):
    skills_pattern = re.compile(r'Skills\s*[:\n]', re.IGNORECASE)
    skills_match = skills_pattern.search(resume_content)

    if skills_match:
        skills_start = skills_match.end()
        skills_end = resume_content.find('\n\n', skills_start)
        skills_section = resume_content[skills_start:skills_end].strip()
        skills_lines = skills_section.split('\n')

        extracted_skills = []
        for line in skills_lines:
            line_skills = re.split(r'[:,-]', line)
            extracted_skills.extend([skill.strip() for skill in line_skills if skill.strip()])

        skills = list(set(extracted_skills))
    else:
        skills = []

    skills = ", ".join(skills)

    RESUME_SECTIONS = [
        "Contact Information", "Objective", "Summary", "Education", "Experience", 
        "Skills", "Projects", "Certifications", "Licenses", "Awards", "Honors", 
        "Publications", "References", "Technical Skills", "Computer Skills", 
        "Programming Languages", "Software Skills", "Soft Skills", "Language Skills", 
        "Professional Skills", "Transferable Skills", "Work Experience", 
        "Professional Experience", "Employment History", "Internship Experience", 
        "Volunteer Experience", "Leadership Experience", "Research Experience", 
        "Teaching Experience",
    ]

    experience_start = resume_content.find("Experience")
    if experience_start == -1:
        return ""

    experience_end = len(resume_content)
    for section in RESUME_SECTIONS:
        if section != "Experience":
            section_start = resume_content.find(section, experience_start)
            if section_start != -1:
                experience_end = min(experience_end, section_start)

    experience_section = resume_content[experience_start:experience_end].strip()

    cleaned_experience = clean_text(experience_section)

    cleaned_skills = clean_text(skills)


    return cleaned_experience + cleaned_skills

def compute_similarity(cleaned_resume, cleaned_jd):

    model = SentenceTransformer('all-MiniLM-L6-v2')
    sentences = [cleaned_resume, cleaned_jd]
    embeddings1 = model.encode(sentences[0])
    embeddings2 = model.encode(sentences[1])
    
    similarity_score = model.similarity(embeddings1, embeddings2)

    return similarity_score
    