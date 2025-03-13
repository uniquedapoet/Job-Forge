
from pdf2image import convert_from_path
import pytesseract
import re
# Accepts PDF/DOCX uploads.
# Extracts text and runs AI-based improvements.


def extract_text_from_pdf(pdf_path):
    # Convert PDF pages to images
    pages = convert_from_path(pdf_path, 500)

    text = ''
    for page in pages:
        text += pytesseract.image_to_string(page)

    return clean_resume_text(text)

def clean_resume_text(text):
    # Replace unwanted characters with a space or appropriate formatting
    text = re.sub(r'[«¢]', '-', text)  # Replace unusual bullets with standard "-"
    text = re.sub(r'(?<!\w)D>[. ]{2,}', '', text)  
    text = text.replace('--','-')

    return text.strip()

def detect_dominant_header_format(text):
    lines = text.split('\n')

    # Patterns to check
    patterns = {
        'all_caps': r'^[A-Z\s]{3,}$',
        'colon_headers': r'^[A-Z][a-z]+.*:$',
        'mixed_case': r'^[A-Z][a-z]+(?: [A-Z][a-z]+)*$'
    }

    # Count occurrences of each pattern
    pattern_counts = {key: 0 for key in patterns}

    for line in lines:
        line = line.strip()
        for key, pattern in patterns.items():
            if re.match(pattern, line):
                pattern_counts[key] += 1

    # Choose the pattern with the highest count
    dominant_pattern = max(pattern_counts, key=pattern_counts.get)
    return patterns[dominant_pattern] if pattern_counts[dominant_pattern] > 0 else None


def extract_resume_sections(text):
    # Define flexible patterns for detecting section headers
    # header_pattern = r'(?:(?:^[A-Z\s]{3,}$)|(?:^[A-Z][a-z]+(?: [A-Z][a-z]+)*:))'
    header_pattern = detect_dominant_header_format(text)

    # Split text into lines for better header detection
    lines = text.split('\n')

    sections = {}
    current_section = 'Summary'  # Default section if no header detected
    sections[current_section] = ''

    for line in lines:
        line = line.strip()
        if re.match(header_pattern, line):
            current_section = line.replace(':', '').strip()
            sections[current_section] = ''
        else:
            sections[current_section] += line + ' '

    # Clean up extra spaces
    for section in sections:
        sections[section] = sections[section].strip()

    return sections
