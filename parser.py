import re
import spacy
import docx2txt
from PyPDF2 import PdfReader

nlp = spacy.load("en_core_web_sm")

def extract_text_from_file(file_path: str):
    if file_path.endswith('.pdf'):
        text = ""
        with open(file_path, "rb") as f:
            pdf = PdfReader(f)
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    elif file_path.endswith('.docx'):
        return docx2txt.process(file_path)
    else:
        raise ValueError("Unsupported file format. Use PDF or DOCX.")

def parse_resume_text(text: str):
    # Basic fields
    name = None
    email = None
    phone = None
    skills = []
    education = []
    experience = []

    # Email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    if email_match:
        email = email_match.group(0)

    # Phone
    phone_match = re.search(r'\+?\d[\d \-]{8,}\d', text)
    if phone_match:
        phone = phone_match.group(0)

    # Name (using first PERSON entity in text)
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    # Skills (simple keyword search – you can expand this)
    skill_keywords = ['python', 'java', 'c++', 'sql', 'fastapi', 'flask', 'javascript', 'html', 'css']
    for word in skill_keywords:
        if re.search(r'\b' + re.escape(word) + r'\b', text, re.IGNORECASE):
            skills.append(word)

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "education": education,
        "experience": experience
    }
