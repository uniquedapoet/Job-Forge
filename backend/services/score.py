import re
from sentence_transformers import SentenceTransformer
import string
import nltk
# nltk.download('stopwords')
# nltk.download('punkt_tab')
# nltk.download('wordnet')
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

    def extract_section(self, section_name, next_sections):
        """
        Extracts a section of the resume based on section headers.

        :param section_name: The name of the section to extract.
        :param next_sections: Possible names of the next sections.
        :return: Extracted text of the section.
        """
        pattern = re.compile(rf'{section_name}\s*[:\n]', re.IGNORECASE)
        match = pattern.search(self.raw_resume)

        if not match:
            return ""

        start = match.end()
        end = len(self.raw_resume)

        for next_section in next_sections:
            next_match = re.search(rf'{next_section}\s*[:\n]', self.raw_resume[start:], re.IGNORECASE)
            if next_match:
                end = start + next_match.start()
                break

        section_text = self.raw_resume[start:end].strip()
        return section_text

    def clean_resume(self):
        # Possible section names for skills and experience
        experience_sections = [
            "Work Experience", "Professional Experience", "Employment History",
            "Internship Experience", "Volunteer Experience"
        ]
        skills_sections = ["Skills", "Technical Skills", "Software Skills"]

        next_sections = [
            "Projects", "Certifications", "Licenses", "Awards", "Honors",
            "Publications", "References", "Education", "Objective", "Summary"
        ]

        # Extract sections
        experience_text = ""
        for exp_section in experience_sections:
            experience_text = self.extract_section(exp_section, next_sections)
            if experience_text:
                break

        skills_text = ""
        for skill_section in skills_sections:
            skills_text = self.extract_section(skill_section, next_sections)
            if skills_text:
                break

        # Clean extracted sections
        cleaned_experience = self.clean_text(experience_text) if experience_text else ""
        cleaned_skills = self.clean_text(skills_text) if skills_text else ""

        return cleaned_experience + " " + cleaned_skills

    def compute_similarity(self):
        cleaned_resume = self.clean_resume()
        cleaned_jd = self.clean_text(self.raw_jd)

        model = SentenceTransformer('all-MiniLM-L6-v2')
        sentences = [cleaned_resume, cleaned_jd]
        embeddings1 = model.encode(sentences[0])
        embeddings2 = model.encode(sentences[1])
        
        similarity_score = model.similarity(embeddings1, embeddings2)

        return similarity_score