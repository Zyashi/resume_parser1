import os
from flask import Flask, render_template, request
import pdfplumber
import spacy
import sqlite3

app = Flask(__name__)

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# SQLite setup
conn = sqlite3.connect("resumes.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    skills TEXT,
    education TEXT
)
""")
conn.commit()

# Simple skills and education keywords
SKILLS = ["Python", "Java", "C++", "SQL", "HTML", "CSS", "JavaScript", "Flask", "Django"]
EDUCATION = ["B.Sc", "B.Tech", "M.Sc", "M.Tech", "Bachelor", "Master", "PhD"]

def extract_text(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "N/A"

def extract_skills(text):
    found_skills = [skill for skill in SKILLS if skill.lower() in text.lower()]
    return ", ".join(found_skills) if found_skills else "N/A"

def extract_education(text):
    found_edu = [edu for edu in EDUCATION if edu.lower() in text.lower()]
    return ", ".join(found_edu) if found_edu else "N/A"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "resume" not in request.files:
        return "No file uploaded", 400
    
    file = request.files["resume"]
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    text = extract_text(file_path)
    name = extract_name(text)
    skills = extract_skills(text)
    education = extract_education(text)

    # Save to SQLite
    cursor.execute("INSERT INTO candidates (name, skills, education) VALUES (?, ?, ?)",
                   (name, skills, education))
    conn.commit()

        # Stylish result page
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Resume Parsed</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="{{{{ url_for('static', filename='style.css') }}}}">
    </head>
    <body>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="card shadow p-4">
                        <h3 class="text-center mb-4">Resume Parsed Successfully!</h3>
                        <p><b>Name:</b> {name}</p>
                        <p><b>Skills:</b> {skills}</p>
                        <p><b>Education:</b> {education}</p>
                        <a href="/" class="btn btn-primary w-100 mt-3">Upload Another Resume</a>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True, port=5001)
