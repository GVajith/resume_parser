
from fastapi import FastAPI, UploadFile, File
import shutil
import os
from utils.parser import extract_text_from_file, parse_resume_text

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    # Save the uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        text = extract_text_from_file(file_path)
        parsed_data = parse_resume_text(text)
        return {"status": "success", "data": parsed_data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        os.remove(file_path)  # cleanup temp file
