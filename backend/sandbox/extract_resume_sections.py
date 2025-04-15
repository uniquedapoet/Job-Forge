import re
import os
from services.resume_scraper import extract_text_from_pdf, extract_resume_sections

def is_title(line):
    if not line or line.startswith('-'):
        return False

    # Heuristic 1: Common separators
    contains_separator = '|' in line or '@' in line

    # Heuristic 2: Dates (e.g., May 2022)
    contains_date = bool(re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}', line))

    # Heuristic 3: Enough long, capitalized words
    words = line.split()
    long_cap_words = [word for word in words if word[0].isupper() and len(word) > 3 and word.isalpha()]
    capitalized_ratio = len(long_cap_words) >= max(1, len(words) // 2)

    return contains_separator or contains_date or capitalized_ratio

def clean_sections(section_lines):
    cleaned = []
    current_bullet = ''
    current_description = ''

    for line in section_lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith('- '):  # Start of a new bullet
            if current_bullet:
                cleaned.append(current_bullet.strip())
            if current_description:
                cleaned.append(current_description.strip())
                current_description = ''
            current_bullet = line

        elif is_title(line):  # Detected a new title
            if current_bullet:
                cleaned.append(current_bullet.strip())
                current_bullet = ''
            if current_description:
                cleaned.append(current_description.strip())
                current_description = ''
            cleaned.append(line)

        elif current_bullet:  # Continuing bullet point
            current_bullet += ' ' + line

        else:  # Description or long sentence across multiple lines
            current_description += ' ' + line if current_description else line

    # Add any remaining lines
    if current_bullet:
        cleaned.append(current_bullet.strip())
    if current_description:
        cleaned.append(current_description.strip())

    return cleaned

def parse_resume_sections(resume_text):
    # Normalize newlines and split into lines
    lines = [line.strip() for line in resume_text.strip().split('\n') if line.strip()]
    
    # Common section headers to detect
    section_titles = [
        'Education', 'Experience', 'Projects', 'Skills', 'Objective', 'Summary',
        'Certifications', 'Awards', 'Activities', 'Languages', 'Publications'
    ]

    # Compile regex for matching section titles
    section_pattern = re.compile(r'^(' + '|'.join(section_titles) + r')$', re.IGNORECASE)
    
    resume_dict = {}
    current_section = "Header"
    resume_dict[current_section] = []

    for line in lines:
        if section_pattern.match(line):
            current_section = line.strip()
            resume_dict[current_section] = []
        else:
            resume_dict[current_section].append(line)

    # Clean each section
    for section, content in resume_dict.items():
        resume_dict[section] = clean_sections(content)

    return resume_dict

resume_file_name = 'EduardoBenjaminResume-1Page-3.pdf'
# 'Giemza_Jackson_Resume.pdf'

RESUME_PATH = os.path.join("data", "resumes", resume_file_name)
raw_resume = extract_text_from_pdf(RESUME_PATH)


sections = parse_resume_sections(raw_resume)

