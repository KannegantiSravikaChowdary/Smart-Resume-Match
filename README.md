# Smart Resume Match
Smart Resume Match is an AI-powered tool built for students, freshers, and job seekers to intelligently match their resumes with job descriptions. It helps identify strengths, highlight skill gaps, suggest improvements

## 🚀 Key Features

- ✅ **Matching Score** — overall percentage alignment between resume and job description  
- 🎓 **Education Match** — detects and compares education requirements in the JD vs. resume  
- 🛠️ **Skill Match** — highlights overlapping skills  
- ⚠️ **Skill Gap** — identifies missing skills and recommends resources  
- ✨ **Enhanced Resume** — uses GenAI to rewrite resume content to better fit the JD  
- 📝 **Edit Option** — allows manual editing of enhanced resume suggestions  
- 🎤 **Interview Questions** — generates 5 personalized, probable interview questions based on your resume & JD  
## 💡 Tech Stack

- **Frontend**: Streamlit  
- **Backend**: Python  
- **Libraries**: 
  - NLP: `nltk`, `spacy`
  - GenAI: `openai`
  - PDF Parsing: `PyMuPDF (fitz)`
  - Matching: `scikit-learn`, `re`
## 🗂️ Project Structure
```smart-resume-match/
│
├── App.py                   # 🚀 Main Streamlit app entry point
├── AppHandler.py            # 🧠 Core logic: text extraction, skill match, education match
├── Enhancer.py              # ✨ Resume enhancement using GenAI (Gemini)
├── GeminiTips.py            # 💡 AI-generated tips for resume improvement
├── Match.py                 # 📊 Score calculation: skill match %, gaps, education alignment
├── SkillExtractor.py        # 🔍 Extracts skills from text using regex + synonyms
├── Skills.json              # 🗂️  Categorized domain-specific skills list
├── requirements.txt         # 📦 Python dependencies
├── .gitignore               # 🚫 Ignore `.env`, cache, etc.
│
├── SampleJD/                # 📝 Sample Job Descriptions (PDF or TXT)
│   └── jd_example.pdf
│
├── SampleResume/            # 📄 Sample Student Resumes (PDF format)
│   └── resume_example.pdf
│
├── .env                     # 🔐 Gemini API Key (ignored from GitHub)
│
└── README.md                # 📘 Project overview, instructions, and documentation```

## ⚙️ Setup Instructions

```bash
git clone https://github.com/your-username/smart-resume-match.git
cd smart-resume-match
pip install -r requirements.txt
streamlit run app.py

## 🔐 Environment Variables (`.env`)

This file is ignored from GitHub using .gitignore.

✅ Store your Gemini API Key securely here.

❌ Never commit .env to any public repository.

