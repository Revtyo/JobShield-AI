from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
from analyzer import (
    get_application_strength, 
    check_ai_genericity, 
    check_ats_compliance, 
    get_universal_keywords
)

app = FastAPI()

# CORS must be configured before routes for extensions to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_job(
    resume_file: UploadFile = File(...), # Handles the PDF binary
    job_description: str = Form(...)      # Handles the scraped text
):
    # 1. Extract text from the uploaded PDF
    resume_bytes = await resume_file.read()
    doc = fitz.open(stream=resume_bytes, filetype="pdf")
    resume_text = "".join([page.get_text() for page in doc])
    
    # 2. Run the Analysis Logic
    strength = get_application_strength(resume_text, job_description)
    ai_check = check_ai_genericity(resume_text)
    ats_check = check_ats_compliance(resume_text)
    missing_gaps = get_universal_keywords(resume_text, job_description)
    
    # 3. Return a unified JSON response to the extension
    return {
        "probability_score": strength,
        "ai_risk": ai_check["status"],
        "perplexity": ai_check["score"],
        "ats_status": ats_check["status"],
        "ats_flags": ats_check["flags"],
        "missing_keywords": missing_gaps
    }