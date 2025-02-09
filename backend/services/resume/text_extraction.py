import pymupdf4llm
import os

md_text = pymupdf4llm.to_markdown(r"C:\Projects\Job-Forge\backend\services\resume\Jackson_Giemza_Resume_2024.pdf")

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resume.md")

with open(file_path, "w", encoding="utf-8") as md_file:
    md_file.write(md_text)


