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

    return text


def extract_resume_sections(text):
    # Define flexible patterns for detecting section headers
    header_pattern = r'(?:(?:^[A-Z\s]{3,}$)|(?:^[A-Z][a-z]+(?: [A-Z][a-z]+)*:))'
    # header_pattern = detect_header_format(text)

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
