import fitz  # PyMuPDF
import json
import re

# Load skills.json
with open("skills.json", "r") as f:
    skill_dict = json.load(f)

SKILL_LIST = set(skill for sublist in skill_dict.values() for skill in sublist)

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = " ".join([page.get_text() for page in doc])
    return text

def extract_skills_from_text(text):
    text = text.lower()

    skills_section = re.findall(r"skills[:\-\s]*([\s\S]{0,400})", text)
    skills_text = " ".join(skills_section) if skills_section else text

    if not skills_section:
        project_skills = re.findall(r"(project[s]?[\s\S]{0,600})", text)
        skills_text += " ".join(project_skills)

    extracted = set()
    for skill in SKILL_LIST:
        if re.search(rf"\b{re.escape(skill.lower())}\b", skills_text):
            extracted.add(skill)

    return list(extracted)
