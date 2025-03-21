import re
from sentence_transformers import SentenceTransformer
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

class Score:
    def __init__(self, raw_resume, raw_jd):
        self.raw_resume = raw_resume
        self.raw_jd = raw_jd

        self.set_of_stopwords = set(stopwords.words("english") + list(string.punctuation))

        self.lemmatizer = WordNetLemmatizer()

    def clean_text(self, raw_text):        

        # Convert text to lowercase and tokenize into words
        tokens = word_tokenize(raw_text.lower())
        # Remove stopwords and punctuation
        tokens = [token for token in tokens if token not in self.set_of_stopwords]
        # Lemmatize the remaining words
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        # Join the tokens back into a single string
        cleaned_text = " ".join(tokens)
        return cleaned_text

    def clean_resume(self):
        skills_pattern = re.compile(r'Skills\s*[:\n]', re.IGNORECASE)
        skills_match = skills_pattern.search(self.raw_resume)

        if skills_match:
            skills_start = skills_match.end()
            skills_end = self.raw_resume.find('\n\n', skills_start)
            skills_section = self.raw_resume[skills_start:skills_end].strip()
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

        experience_start = self.raw_resume.find("Experience")
        if experience_start == -1:
            return ""

        experience_end = len(self.raw_resume)
        for section in RESUME_SECTIONS:
            if section != "Experience":
                section_start = self.raw_resume.find(section, experience_start)
                if section_start != -1:
                    experience_end = min(experience_end, section_start)

        experience_section = self.raw_resume[experience_start:experience_end].strip()
        cleaned_experience = self.clean_text(experience_section)
        cleaned_skills = self.clean_text(skills)

        return cleaned_experience + cleaned_skills

    def compute_similarity(self):
        cleaned_resume = self.clean_resume()
        cleaned_jd = self.clean_text(self.raw_jd)

        model = SentenceTransformer('all-MiniLM-L6-v2')
        sentences = [cleaned_resume, cleaned_jd]
        embeddings1 = model.encode(sentences[0])
        embeddings2 = model.encode(sentences[1])
        
        similarity_score = model.similarity(embeddings1, embeddings2)

        return similarity_score