import os
import google.generativeai as genai
from dotenv import load_dotenv
import re

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Resume Enhancer ---
def enhance_resume(resume_text, jd_text):
    prompt = f"""
    Enhance the following resume to closely align with the provided job description.

    --- Job Description ---
    {jd_text}

    --- Original Resume ---
    {resume_text}

    ✍️ Rewrite the resume to:
    - Emphasize relevant skills and experience
    - Align terminology with the JD
    - Keep formatting clean and ATS-friendly

    Provide the output as a complete, improved resume.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error enhancing resume: {e}"

# --- Resume Summary Generator ---
def generate_resume_summary(resume_text):
    prompt = f"""
    You are a professional resume coach. Read the resume below and write a short, confident 4-5 line summary for a final-year student.

    --- Resume ---
    {resume_text}

    Only return the summary. Do not include headings or extra commentary.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "⚠️ Could not generate summary."
def course_recommendations(missing_skills):
    if not missing_skills:
        return "🎉 Great job! Your resume covers all the key skills for this job."

    # Trim skills list to avoid token overflow or vague answers
    trimmed_skills = missing_skills[:5]

    prompt = f"""
Suggest **2 beginner-friendly online courses** for each of the following missing skills: {', '.join(missing_skills)}. Return in this vertical markdown format:

For each course, give:
- ✅ Course title  
- 🌐 Platform  
- 📎 One-line reason it's useful

🔹 Skill: <Skill Name>  
✅ Course 1: <Course Title>  
🌐 Platform: <Platform>  
📎 Why: <One-line reason>  

✅ Course 2: <Course Title>  
🌐 Platform: <Platform>  
📎 Why: <One-line reason>  

Repeat the above format per skill.  
Use line breaks between all points. No paragraphs. No extra commentary.

Return only the clean markdown output, no explanations.
"""


    try:
        response = model.generate_content(prompt)

        # Check for valid output
        if not hasattr(response, "text") or not response.text.strip():
            return "❌ No course recommendations were generated. (Empty response)"
        
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error generating course recommendations: {e}"
# --- Interview Questions Based on JD + Resume ---
def suggest_questions(jd_text, resume_text):
    prompt = f"""
You are an expert technical interviewer. Based on the job description and resume below, generate 5 probable interview questions for the candidate.

### JOB DESCRIPTION:
{jd_text}

### RESUME:
{resume_text}

Only return the list of questions. No explanations.
"""
    
    try:
        response = model.generate_content(prompt)
        questions_raw = response.text.strip().split('\n')

        questions = []
        for q in questions_raw:
            cleaned = re.sub(r"^\s*(Q?\d+[\.\)]\s*)+", "", q).strip()
            if cleaned:
                questions.append(cleaned)

        return questions

    except Exception as e:
        return [f"⚠️ Error generating questions: {e}"]