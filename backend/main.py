from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

import google.generativeai as genai
from gtts import gTTS
from PyPDF2 import PdfReader
import docx

import json
import os
import hashlib
import re

# ----------- APP SETUP -----------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("audio", exist_ok=True)

# ----------- CREDENTIALS -----------

GEMINI_API_KEY = "AIzaSyCZulFrxKehEio8KeUci8N_byn9ib1lZYQ"

# ----------- GEMINI SETUP -----------

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.0-flash")
print("Gemini API configured successfully!")

# ----------- REQUEST MODEL -----------

class TextRequest(BaseModel):
    text: str

# ----------- DOCUMENT CHUNKING -----------

def chunk_text(text, max_chunk_size=4000):
    """Split text into chunks at sentence boundaries."""
    if len(text) <= max_chunk_size:
        return [text]

    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:
            current_chunk += (" " + sentence if current_chunk else sentence)
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks if chunks else [text[:max_chunk_size]]

# ----------- LLM GENERATION -----------

def generate_with_gemini(prompt_text):
    """Generate text using Gemini API."""
    response = gemini_model.generate_content(prompt_text)
    return response.text.strip()

# ----------- SIMPLIFICATION -----------

SIMPLIFY_PROMPT = """Simplify the following legal text into plain English. Extract every key detail.

You MUST capture ALL of the following if present:
- Parties involved (names, roles)
- Effective dates, start dates, end dates, renewal dates
- Payment amounts, fees, interest rates, penalties for late payment
- Obligations and responsibilities of each party
- Rights granted to each party
- Termination conditions and notice periods
- Confidentiality or non-disclosure requirements
- Non-compete or exclusivity clauses
- Limitation of liability and indemnification terms
- Warranty or guarantee terms
- Governing law and jurisdiction
- Dispute resolution method (arbitration, mediation, court)
- Intellectual property ownership
- Data privacy and usage terms
- Force majeure or exception clauses
- Amendment and modification procedures
- Any numerical values: dollar amounts, percentages, time periods, quantities

Rules:
- Use short bullet points, each under 20 words
- Use plain simple English, no legal jargon
- Do NOT skip any clause or section
- Do NOT merge unrelated points into one bullet
- Preserve all specific numbers, dates, names, and amounts exactly

Legal text:
{text}

Simplified version:"""


def simplify_full_document(text):
    """Chunk and simplify a full document."""
    chunks = chunk_text(text)
    simplified_parts = []

    for chunk in chunks:
        prompt = SIMPLIFY_PROMPT.format(text=chunk)
        result = generate_with_gemini(prompt)
        simplified_parts.append(result.strip())

    return "\n\n".join(simplified_parts)

# ----------- RISK ANALYSIS -----------

RISK_PROMPT = """Analyze the following legal text and identify every potential risk for the person signing or agreeing to these terms.

Check carefully for ALL of these risk categories:
- Financial risks: hidden fees, penalties, price escalation, payment obligations, late charges
- Liability risks: unlimited liability, indemnification obligations, assumption of risk
- Termination risks: auto-renewal, difficult exit clauses, early termination penalties
- Privacy risks: broad data collection, data sharing with third parties, surveillance
- IP risks: transfer of intellectual property rights, broad licensing grants
- Legal risks: unfavorable jurisdiction, mandatory arbitration, class action waiver
- Obligation risks: non-compete clauses, exclusivity, restrictive covenants
- Warranty risks: "as-is" disclaimers, no warranty, limitation of remedies
- Time-sensitive risks: short notice periods, tight deadlines, auto-renewal windows
- One-sided terms: unilateral amendment rights, unilateral termination rights

For EACH risk found provide:
1. title: A short title (3-6 words)
2. level: "High", "Medium", or "Low"
3. description: 1-2 sentences explaining the risk and its impact

Return ONLY valid JSON in this exact format:
{{"risks": [{{"title": "...", "level": "High", "description": "..."}}]}}

If no risks found return: {{"risks": []}}

Legal text:
{text}

JSON:"""


def analyze_risks(text):
    """Analyze risks in legal text using chunking."""
    chunks = chunk_text(text)
    all_risks = []

    for chunk in chunks:
        prompt = RISK_PROMPT.format(text=chunk)
        raw = generate_with_gemini(prompt)

        try:
            start = raw.find("{")
            end = raw.rfind("}") + 1
            if start != -1 and end > start:
                parsed = json.loads(raw[start:end])
                risks = parsed.get("risks", [])
                all_risks.extend(risks)
        except (json.JSONDecodeError, ValueError):
            pass

    return all_risks

# ----------- TAMIL TRANSLATION (GEMINI) -----------

def translate_to_tamil(text):
    """Translate text to Tamil using Gemini API."""
    try:
        prompt = (
            "Translate the following English text into simple spoken Tamil. "
            "Keep the translation natural and easy to understand. "
            "Return ONLY the Tamil translation, nothing else.\n\n"
            f"Text:\n{text}"
        )
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return ""

# ----------- AUDIO GENERATION -----------

def generate_audio(text, request):
    """Generate audio and return the URL."""
    if not text:
        return ""

    file_hash = hashlib.md5(text.encode()).hexdigest()
    file_path = f"audio/{file_hash}.mp3"

    if not os.path.exists(file_path):
        tts = gTTS(text=text, lang="en")
        tts.save(file_path)

    base_url = str(request.base_url).rstrip("/")
    return f"{base_url}/audio/{file_hash}.mp3"

# ----------- FILE TEXT EXTRACTION -----------

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def extract_text_from_file(file: UploadFile):
    """Extract text from uploaded file."""
    filename = file.filename.lower()
    ext = os.path.splitext(filename)[1]

    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    if ext == ".pdf":
        pdf = PdfReader(file.file)
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif ext == ".docx":
        doc = docx.Document(file.file)
        text = "\n".join(para.text for para in doc.paragraphs)
    else:
        text = file.file.read().decode("utf-8")

    return text.strip()

# ----------- API ENDPOINTS -----------

@app.post("/simplify/")
async def simplify_text_endpoint(request: Request, text_request: TextRequest):
    if not text_request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    try:
        simplified = simplify_full_document(text_request.text)
        tamil = translate_to_tamil(simplified)
        audio_url = generate_audio(simplified, request)

        return {
            "simplified_text": simplified,
            "tamil_text": tamil,
            "audio_url": audio_url,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to simplify text: {str(e)}"
        )


@app.post("/upload/")
async def upload_file_endpoint(request: Request, file: UploadFile = File(...)):
    try:
        extracted_text = extract_text_from_file(file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not extracted_text:
        raise HTTPException(
            status_code=400,
            detail="No text could be extracted from the uploaded file.",
        )

    try:
        simplified = simplify_full_document(extracted_text)
        tamil = translate_to_tamil(simplified)
        audio_url = generate_audio(simplified, request)

        return {
            "simplified_text": simplified,
            "tamil_text": tamil,
            "audio_url": audio_url,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process uploaded file: {str(e)}"
        )


@app.post("/risk-analysis/")
async def risk_analysis_text_endpoint(request: Request, text_request: TextRequest):
    if not text_request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    try:
        risks = analyze_risks(text_request.text)
        return {"risks": risks}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to analyze risks: {str(e)}"
        )


@app.post("/risk-analysis/upload/")
async def risk_analysis_upload_endpoint(
    request: Request, file: UploadFile = File(...)
):
    try:
        extracted_text = extract_text_from_file(file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not extracted_text:
        raise HTTPException(
            status_code=400,
            detail="No text could be extracted from the uploaded file.",
        )

    try:
        risks = analyze_risks(extracted_text)
        return {"risks": risks}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to analyze risks: {str(e)}"
        )


@app.get("/audio/{filename}")
async def get_audio(filename: str):
    file_path = os.path.join("audio", filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found.")

    return FileResponse(file_path, media_type="audio/mpeg")
