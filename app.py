import os
import re
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from io import BytesIO
from typing import Tuple, List, Set

from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity

import PyPDF2
from docx import Document

ALLOWED_EXTENSIONS = { 'pdf', 'docx', 'txt' }

app = Flask(__name__)
app.secret_key = 'dev-secret'  # replace in production
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ---------------------- Utils ----------------------

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_text(text: str) -> str:
    # Basic cleanup
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_text_from_pdf(file_stream) -> str:
    try:
        reader = PyPDF2.PdfReader(file_stream)
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        return "\n".join(pages)
    except Exception:
        return ""

def extract_text_from_docx(file_stream) -> str:
    try:
        # python-docx needs a file path or a file-like object with seek
        data = file_stream.read()
        file_stream.seek(0)
        bio = BytesIO(data)
        doc = Document(bio)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception:
        return ""

def extract_text_from_txt(file_stream) -> str:
    try:
        data = file_stream.read()
        if isinstance(data, bytes):
            try:
                return data.decode('utf-8', errors='ignore')
            except Exception:
                return data.decode('latin-1', errors='ignore')
        return data
    except Exception:
        return ""

def read_any(file_storage) -> str:
    filename = file_storage.filename
    ext = filename.rsplit('.', 1)[1].lower()
    if ext == 'pdf':
        return extract_text_from_pdf(file_storage.stream)
    elif ext == 'docx':
        return extract_text_from_docx(file_storage.stream)
    elif ext == 'txt':
        return extract_text_from_txt(file_storage.stream)
    return ""

def jd_and_resume_from_request() -> Tuple[str, str, List[str]]:
    reasons = []

    resume_text = ""
    jd_text = ""

    # Resume: file required
    resume_file = request.files.get('resume_file')
    if resume_file and resume_file.filename and allowed_file(resume_file.filename):
        resume_text = read_any(resume_file)
        if not resume_text.strip():
            reasons.append("Couldn't read text from the resume file.")
    else:
        reasons.append("Please upload a resume (PDF/DOCX/TXT).")

    # JD: either pasted text or uploaded file
    jd_text = request.form.get('jd_text', '').strip()
    jd_file = request.files.get('jd_file')
    if not jd_text and jd_file and jd_file.filename and allowed_file(jd_file.filename):
        jd_text = read_any(jd_file)
        if not jd_text.strip():
            reasons.append("Couldn't read text from the JD file. Try pasting the JD text instead.")

    if not jd_text:
        reasons.append("Provide a Job Description (paste text or upload a file).")

    return clean_text(jd_text), clean_text(resume_text), reasons

def compute_similarity(jd_text: str, resume_text: str) -> float:
    # Use TF-IDF with English stopwords
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf = vectorizer.fit_transform([jd_text, resume_text])
        sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return float(sim)
    except ValueError:
        return 0.0

def tokenize(text: str) -> List[str]:
    # Simple tokenization
    words = re.findall(r"[a-zA-Z][a-zA-Z+.#/\-]*", text.lower())
    return [w for w in words if w not in ENGLISH_STOP_WORDS and len(w) > 2]

def top_missing_keywords(jd_text: str, resume_text: str, top_n: int = 20) -> List[str]:
    # Get candidate keywords from JD that are absent in resume
    jd_tokens = tokenize(jd_text)
    res_tokens = set(tokenize(resume_text))

    # Basic frequency scoring in JD
    from collections import Counter
    counts = Counter(jd_tokens)
    # Prefer tokens not in resume
    missing = [(tok, cnt) for tok, cnt in counts.items() if tok not in res_tokens]
    # Sort by frequency (desc) and then alpha
    missing.sort(key=lambda x: (-x[1], x[0]))
    return [tok for tok, _ in missing[:top_n]]

def suggest_bullets(missing: List[str]) -> List[str]:
    bullets = []
    for kw in missing[:8]:
        bullets.append(f"Implemented and optimized {kw} solutions, driving measurable impact and aligning with business goals.")
    return bullets

# ---------------------- Routes ----------------------

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    jd_text, resume_text, reasons = jd_and_resume_from_request()
    if reasons:
        for r in reasons:
            flash(r, 'error')
        return redirect(url_for('index'))

    score = compute_similarity(jd_text, resume_text)
    percent = round(score * 100, 1)

    missing = top_missing_keywords(jd_text, resume_text, top_n=25)
    bullets = suggest_bullets(missing)

    return render_template('result.html',
                           score_percent=percent,
                           missing_keywords=missing,
                           bullets=bullets,
                           jd_preview=jd_text[:1200],
                           resume_preview=resume_text[:1200])

if __name__ == '__main__':
    app.run(debug=True)
