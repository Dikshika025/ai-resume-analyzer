## 🧠 About This Project

The *AI Resume Analyzer* is an intelligent web application built using *Flask* and *Natural Language Processing (NLP)* that helps job seekers tailor their resumes for specific job descriptions.  
It compares the candidate’s resume with a given JD (Job Description), calculates a *match score, and highlights **missing keywords* or *skills gaps* to improve resume alignment.  

🔹 *Key Features*
- Upload resumes in *PDF, DOCX, or TXT* format  
- Paste or upload a *Job Description* for analysis  
- Uses *TF-IDF based similarity* for scoring (can be extended with BERT or spaCy)  
- Displays clear results on skills alignment and missing areas  

🛠 *Tech Stack*
- *Python, **Flask* — Backend  
- *NLTK / Scikit-learn* — NLP processing  
- *HTML / CSS / Bootstrap* — Frontend  

🚀 *Goal*: Help candidates optimize their resumes and improve interview shortlisting chances using AI-driven text analysis.
# 🧠 AI Resume Analyzer (Flask + NLP)

A web app that helps you analyze your *resume* against a *job description* using Natural Language Processing (NLP).

It compares the two documents and shows:
- ✅ Match percentage
- 🔍 Missing keywords
- 💡 Suggestions for improvement

---

## 🚀 Features
- Upload Resume (PDF / DOCX / TXT)
- Paste or upload Job Description
- Automatic text extraction & keyword comparison
- Shows similarity score between resume and JD
- Highlights missing skills and suggestions

---

## 🛠 Tech Stack
- *Python*  
- *Flask* (Backend framework)  
- *NLTK / Scikit-learn* (NLP processing)  
- *HTML / CSS / Bootstrap* (Frontend)  

---

## ⚙ How to Run Locally

### ⿡ Create a Python environment
*Windows (PowerShell):*
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1

## 🖼 Project Screenshots

### 🔹 Home Page (Top)
![Home Page Top](home_top.png)

### 🔹 Home Page (Bottom)
![Home Page Bottom](home_bottom.png)