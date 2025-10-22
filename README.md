
# AI Resume Analyzer (Flask + NLP)

A lightweight web app that:
- Parses a resume (PDF/DOCX/TXT)
- Compares it with a Job Description (paste text or upload)
- Gives a match score, highlights missing keywords, and suggests improvements

## Quick Start

### 1) Create a Python environment
**Windows (PowerShell):**
```
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
```
pip install -r requirements.txt
```

### 3) Run the app
```
python app.py
```
Open http://127.0.0.1:5000 in your browser.

### 4) Use it
- Upload your resume (PDF/DOCX/TXT).
- Paste the Job Description (or upload a JD file).
- Click **Analyze** to see: similarity score, missing keywords, and suggested bullet points.

## Tips
- Keep your resume as text-rich PDF (not just a scanned image).
- For better results, provide a full JD.
- This is a starter—you can plug in spaCy, BERT, or embeddings later.
=======
# ai-resume-analyzer
AI Resume Analyzer — A Flask-based web app that compares your resume with a job description using NLP and shows match score, missing keywords, and suggestions.
>>>>>>> b8f40cecbeb578c3130e93bd5d01e6af1b1e1e97
