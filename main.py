# main.py

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from utils.analyzer import analyze_resume_with_ollama, match_resume_to_job
from utils.extractor import extract_text_from_pdf
from fastapi.responses import JSONResponse
from fpdf import FPDF
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
import tempfile

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or replace "*" with ["http://127.0.0.1:5500"] for stricter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Optional: Keep old APIs for debugging
class ResumeText(BaseModel):
    text: str

class JobMatchInput(BaseModel):
    resume: str
    job_description: str


# ✅ New: Upload PDF resume, analyze directly
@app.post("/analyze-pdf")
async def analyze_pdf_resume(file: UploadFile = File(...)):
    contents = await file.read()
    extracted = extract_text_from_pdf(contents)
    return analyze_resume_with_ollama(extracted)


# ✅ New: Upload resume PDF + JD (PDF or TXT)
@app.post("/match-files")
async def match_resume_and_job(
    resume_file: UploadFile = File(...),
    jd_file: UploadFile = File(None),
    jd_text: str = Form(None)
):
    resume_content = await resume_file.read()
    resume_text = extract_text_from_pdf(resume_content)

    jd_text_final = None

    # ✅ If JD file is a real file (not a blank string from Swagger or curl)
    if jd_file and getattr(jd_file, "filename",None):
        jd_content = await jd_file.read()
        if jd_file.filename.endswith(".pdf"):
            jd_text_final = extract_text_from_pdf(jd_content)
        else:
            jd_text_final = jd_content.decode("utf-8")

    # ✅ Fallback to JD text if no valid JD file
    if not jd_text_final and jd_text:
        jd_text_final = jd_text

    # ❌ If neither input is valid
    if not jd_text_final:
        raise HTTPException(status_code=400, detail="Provide either JD PDF/text file or JD plain text.")

    return match_resume_to_job(resume_text, jd_text_final)

    

# 🔖 Export any analysis or match result to JSON
@app.post("/download/json")
def download_as_json(data: dict):
    return JSONResponse(content=data)


# 🔖 Export any analysis or match result to PDF
@app.post("/download/pdf")
def download_as_pdf(data: dict):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    def add_lines(obj, indent=0):
        for k, v in obj.items():
            if isinstance(v, list):
                pdf.cell(0, 10, f"{' ' * indent}{k}:", ln=True)
                for item in v:
                    line = item if isinstance(item, str) else str(item)
                    pdf.cell(0, 10, f"{' ' * (indent + 2)}- {line}", ln=True)
            elif isinstance(v, dict):
                pdf.cell(0, 10, f"{' ' * indent}{k}:", ln=True)
                add_lines(v, indent + 2)
            else:
                pdf.cell(0, 10, f"{' ' * indent}{k}: {v}", ln=True)

    add_lines(data)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    with open(temp_file.name, "rb") as f:
        pdf_data = f.read()
    return Response(pdf_data, media_type="application/pdf", headers={
        "Content-Disposition": "attachment; filename=result.pdf"
    })

