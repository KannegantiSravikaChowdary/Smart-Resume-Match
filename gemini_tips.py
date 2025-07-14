import re
import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv


# Configure Gemini model

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def suggestions_resume(missing_skills):
    """
    Returns AI-generated bullet point suggestions for missing skills.
    """
    if not missing_skills:
        return "✅ Your resume aligns perfectly with the job description."

    prompt = f"""
You are an expert resume coach. A student is missing the following skills: {', '.join(missing_skills)}.
Suggest exactly 5 impactful, single-line bullet points they can add to their resume.
Each point should:
- Begin with a strong action verb.
- Be student-friendly (project-based or learning-based).
- Use simple, concise language.
Respond only with 5 bullet points in Markdown format. Do not add any explanation, tips, or headings.
"""

    try:
        response = model.generate_content(prompt)
        if response and response.text:
            return "💡 *AI Suggestions to Improve Resume:*\n\n" + response.text.strip()
    except Exception:
        pass

    # Fallback (fix: flatten the list of lines)
    fallback_points = []
    for skill in missing_skills:
        fallback_points.extend([
            f"- Built a simple project using {skill} and documented it in resume.",
            f"- Learned {skill} through online tutorials and applied it in coursework.",
            f"- Used {skill} in a basic app for solving student-related problems.",
            f"- Explored {skill} by contributing to an open-source GitHub repo.",
            f"- Mentioned {skill} under Technical Skills after completing a course."
        ])

    return "💡 *AI Suggestions to Improve Resume:*\n\n" + "\n".join(fallback_points)
