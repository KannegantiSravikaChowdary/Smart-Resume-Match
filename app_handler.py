import fitz  # PyMuPDF
import json
import os
import re

# === Gemini is used only in enhancer.py, so no GenAI needed here ===

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def load_skills():
    import json
    with open("skills.json", "r") as f:
        data = json.load(f)

    # Flatten all skills into a single list, lowercase, and deduplicated
    all_skills = set()
    for category in data.values():
        all_skills.update(skill.lower() for skill in category)
    
    return list(all_skills)


def extract_skills(text, skills_list, synonyms=None):
    text = text.lower()
    found_skills = set()
    synonyms = synonyms or {}

    for skill in skills_list:
        skill_variants = [skill.lower()] + synonyms.get(skill.lower(), [])
        for variant in skill_variants:
            pattern = r'\b' + re.escape(variant) + r'\b'
            if re.search(pattern, text):
                found_skills.add(skill.lower())
                break
    return list(found_skills)

def extract_degree(text):
    degrees = {
        "btech": ["b.tech", "bachelor of technology", "engineering"],
        "bcom": ["b.com", "bachelor of commerce"],
        "bsc": ["b.sc", "bachelor of science"],
        "msc": ["m.sc", "master of science"],
        "mtech": ["m.tech", "master of technology"],
        "mba": ["mba", "master of business administration"],
    }
    text = text.lower()
    found_degrees = set()
    for key, variants in degrees.items():
        for v in variants:
            if v in text:
                found_degrees.add(key)
                break
    return found_degrees

def check_education(resume_text, jd_text):
    resume_degrees = extract_degree(resume_text)
    jd_degrees = extract_degree(jd_text)
    return bool(resume_degrees & jd_degrees)
