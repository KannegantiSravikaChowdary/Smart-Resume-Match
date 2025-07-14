import streamlit as st
import plotly.graph_objects as go
import fitz  # PyMuPDF
from match import calculate_match
from enhancer import enhance_resume, generate_resume_summary, course_recommendations,suggest_questions
from gemini_tips import suggestions_resume

# --- Page Config ---
st.set_page_config(page_title="Smart Resume Match", layout="wide")

# --- Styling ---
st.markdown("""
<style>
    .stFileUploader {padding: 1.2rem; border: 2px dashed #aaa; background-color: #f8f9fa;}
    .stButton>button, .stDownloadButton>button {background-color: #0072E3; color: white;}
</style>
""", unsafe_allow_html=True)

# --- Session Initialization ---
if 'page' not in st.session_state:
    st.session_state.page = "🏠 Welcome"

for key in ['match_score', 'matched_skills', 'missing_skills', 'edu_match',
            'resume_text', 'jd_text', 'enhanced_resume', 'tips', 'resume_file']:
    st.session_state.setdefault(key, None)

# --- Sidebar Navigation ---
st.sidebar.title("🚀 Smart Navigation")
page = st.sidebar.radio("Go to", [
    "🏠 Welcome",
    "📤 Upload Files",
    "📊 Match Results",
    "✨ AI Tips",
    "🧠 Enhanced Resume",
    "📚 Course Recommendations",
    "🎤 Interview Questions Generator"
], index=["🏠 Welcome", "📤 Upload Files", "📊 Match Results", "✨ AI Tips", "🧠 Enhanced Resume", "📚 Course Recommendations",
    "🎤 Interview Questions Generator"].index(st.session_state.page))
st.session_state.page = page

# --- Header ---
if page != "🏠 Welcome":
    st.markdown("<h1 style='text-align:center;'>🧠 Smart Resume Match</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Check your resume’s alignment with a job description and get AI-based improvement tips.</p>", unsafe_allow_html=True)

# --- Welcome Page ---
if page == "🏠 Welcome":
    st.markdown("""
    <style>
    .hero-background {
        background: linear-gradient(135deg, #f0f4ff 0%, #e0f7fa 100%);
        border-radius: 12px;
        padding: 3rem;
        margin: 3rem auto;
        max-width: 700px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
        text-align: center;
    }
    .hero-icon {
        font-size: 5rem;
        color: #3b82f6;
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e293b;
    }
    .hero-subtitle {
        font-size: 1.25rem;
        color: #475569;
        margin-bottom: 2rem;
    }
    </style>
    <div class="hero-background">
        <div class="hero-icon">🤖📄🚀</div>
        <div class="hero-title">Welcome to Smart Resume Match</div>
        <div class="hero-subtitle">Align your resume with your dream job in minutes using AI-powered insights.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 Get Started"):
        st.session_state.page = "📤 Upload Files"

# --- Upload Files Page ---
elif page == "📤 Upload Files":
    st.subheader("📄 Upload Resume")
    resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"], key="resume")

    st.subheader("📑 Upload Job Description")
    jd_file = st.file_uploader("Upload job description (PDF)", type=["pdf"], key="jd")

    if st.button("🚀 Analyze Match"):
        if not resume_file or not jd_file:
            st.warning("⚠ Please upload both Resume and Job Description.")
        else:
            with st.spinner("Analyzing..."):
                try:
                    result = calculate_match(resume_file, jd_file)
                    st.session_state.resume_file = resume_file  # store original resume
                    st.session_state.match_score = result["match_score"]
                    st.session_state.matched_skills = result["matched_skills"]
                    st.session_state.missing_skills = result["missing_skills"]
                    st.session_state.edu_match = result["education_match"]
                    st.session_state.resume_text = result["raw_resume_text"]
                    st.session_state.jd_text = result["raw_jd_text"]
                    st.session_state.enhanced_resume = enhance_resume(
                        st.session_state.resume_text, st.session_state.jd_text
                    )
                    st.session_state.tips = suggestions_resume(st.session_state.missing_skills) if st.session_state.missing_skills else None
                    st.success("✅ Analysis complete. Use sidebar to view results.")
                except Exception as e:
                    st.error(f"❌ Error during analysis: {e}")

# --- Match Results Page ---
elif page == "📊 Match Results":
    if st.session_state.match_score is not None:
        st.subheader("🔗 Resume–JD Match Score")
        color = "green" if st.session_state.match_score >= 75 else "orange" if st.session_state.match_score >= 50 else "red"
        st.markdown(f"<h2 style='color:{color}'>{st.session_state.match_score}%</h2>", unsafe_allow_html=True)
        st.progress(st.session_state.match_score / 100)

        st.subheader("📊 Skills Match Breakdown")
        matched = len(st.session_state.matched_skills)
        missing = len(st.session_state.missing_skills)

        fig = go.Figure(data=[go.Pie(
            labels=["Matched Skills", "Missing Skills"],
            values=[matched, missing],
            hole=0.5,
            marker=dict(colors=["#10B981", "#EF4444"])
        )])
        fig.update_layout(showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"**✅ Matched Skills ({matched}):**")
        st.success(", ".join(st.session_state.matched_skills) or "None")

        st.markdown(f"**❌ Missing Skills ({missing}):**")
        st.error(", ".join(st.session_state.missing_skills) or "None")

        st.subheader("🎓 Education Match")
        st.info("✅ Degree matched" if st.session_state.edu_match else "❌ No matching degree found")
    else:
        st.info("📥 Please upload and analyze files first.")

# --- AI Tips Page ---
elif page == "✨ AI Tips":
    if st.session_state.tips:
        st.subheader("✨ Skill Improvement Suggestions")
        st.markdown(st.session_state.tips, unsafe_allow_html=True)
        st.download_button("📥 Download Suggestions", st.session_state.tips, file_name="resume_tips.txt")
    else:
        st.info("📥 Upload files and analyze first to see tips.")

# --- Enhanced Resume Page ---
elif page == "🧠 Enhanced Resume":
    if st.session_state.enhanced_resume:
        st.subheader("🧠 AI-Enhanced Resume")

        edited_resume = st.text_area("✏️ Edit your resume here", st.session_state.enhanced_resume, height=400, key="edited_resume")

        st.download_button(
            "📥 Download Edited Resume (Text)",
            edited_resume,
            file_name="Edited_Resume.txt"
        )

        st.subheader("📌 Resume Summary")
        st.info(generate_resume_summary(st.session_state.resume_text))

        st.subheader("📄 Extracted JD")
        st.text(st.session_state.jd_text)
    else:
        st.info("📥 Upload files and analyze first.")

# --- Course Recommendations Page ---
elif page == "📚 Course Recommendations":
    if st.session_state.missing_skills:
        st.subheader("📚 AI-Curated Course Recommendations")
        with st.spinner("🔍 Finding the best learning paths for you..."):
            courses = course_recommendations(st.session_state.missing_skills)
            if courses:
                st.markdown(courses, unsafe_allow_html=True)
                st.download_button("📥 Download Courses", courses, file_name="AI_Courses.txt")
            else:
                st.error("❌ No course recommendations were generated.")
    else:
        st.info("📥 Analyze your resume first to see course suggestions.")
elif page == "🎤 Interview Questions Generator":
    st.subheader("🎤 Interview Questions Generator")

    if st.session_state.jd_text and st.session_state.resume_text:
        with st.spinner("Generating interview questions..."):
            questions = suggest_questions(st.session_state.jd_text, st.session_state.resume_text)
        if questions:
            for i, q in enumerate(questions, 1):
                st.markdown(f"**Q{i}.** {q}")
            st.download_button("📥 Download Questions", "\n".join(questions), file_name="Interview_Questions.txt")
        else:
            st.info("No questions generated.")
    else:
        st.info("Please upload and analyze both Resume and Job Description first.")

# --- Footer ---
st.markdown("---")
st.caption("Made with ❤️ by students for students • Smart Resume Match © 2025") 