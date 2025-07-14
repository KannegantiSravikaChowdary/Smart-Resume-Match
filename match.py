from app_handler import extract_text_from_pdf, extract_skills, check_education, load_skills
import re

def clean_text(text):
    return re.sub(r'\s+', ' ', text.lower())

def calculate_match(resume_file, jd_file):
    skills_list = load_skills()

    resume_text = extract_text_from_pdf(resume_file)
    jd_text = extract_text_from_pdf(jd_file)

    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)

    resume_skills = extract_skills(resume_clean, skills_list)
    jd_skills = extract_skills(jd_clean, skills_list)

    matched = sorted(set(resume_skills) & set(jd_skills))
    missing = sorted(set(jd_skills) - set(resume_skills))

    match_score = round((len(matched) / len(jd_skills)) * 100, 2) if jd_skills else 0.0
    edu_match = check_education(resume_clean,jd_clean)

    result = {
        "match_score": match_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "education_match": edu_match,
        "raw_resume_text": resume_text,
        "raw_jd_text": jd_text
    }

    return result
