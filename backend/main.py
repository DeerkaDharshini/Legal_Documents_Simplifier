# from langchain_ollama import ChatOllama
# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel

# from langchain_community.chat_models import ChatOllama
# from langchain_core.prompts import ChatPromptTemplate

# from gtts import gTTS

# from PyPDF2 import PdfReader
# import docx

# import json
# import os
# import hashlib

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ----------- CREATE AUDIO FOLDER -----------

# os.makedirs("audio", exist_ok=True)

# # ----------- REQUEST MODEL -----------

# class TextRequest(BaseModel):
#     text: str

# # ----------- MODEL -----------

# llm = ChatOllama(
#     model="mistral",
#     temperature=0.1
# )

# # ----------- PROMPT -----------

# prompt = ChatPromptTemplate.from_template("""
# You are a legal document simplifier.

# Your task is to simplify legal text into clear, simple English.

# IMPORTANT RULES:

# If the text is SHORT (1-2 sentences):
# - Convert it into ONE simple sentence
# - Maximum 12 words

# If the text is LONG (document, multiple paragraphs):
# - Extract ALL important information
# - Do NOT summarize into one sentence
# - Convert into multiple short bullet points

# You MUST include:
# • Important rules
# • Deadlines
# • Responsibilities
# • Penalties
# • Rights
# • Important dates
# • Required actions

# Remove:
# • Repeated sentences
# • Legal jargon
# • Unnecessary wording

# Each bullet must:
# - Be clear
# - Be simple
# - Be under 15 words

# Also translate EACH bullet into simple spoken Tamil.

# IMPORTANT :
# Return ONLY valid JSON.


# FORMAT:
# {{
#   "simplified_text": "...",
#   "tamil_text": "..."
# }}

# TEXT:
# {text}
# """)

# # ----------- TEXT INPUT API -----------

# @app.post("/simplify/")
# async def simplify_text(request: TextRequest):
#     try:
#         chain = prompt | llm
#         response = chain.invoke({"text": request.text})

#         raw_output = response.content.strip()

#         try:
#             start = raw_output.find("{")
#             end = raw_output.rfind("}") + 1
#             clean_json = raw_output[start:end]

#             parsed = json.loads(clean_json)

#             simplified = parsed.get("simplified_text", "").strip()
#             tamil = parsed.get("tamil_text", "").strip()

#         except Exception:
#             simplified = raw_output
#             tamil = ""

#         # ----------- AUDIO -----------

#         audio_url = ""

#         if simplified:
#             file_hash = hashlib.md5(simplified.encode()).hexdigest()
#             file_path = f"audio/{file_hash}.mp3"

#             if not os.path.exists(file_path):
#                 tts = gTTS(text=simplified, lang='en')
#                 tts.save(file_path)

#             audio_url = f"http://127.0.0.1:8000/audio/{file_hash}.mp3"

#         return {
#             "simplified_text": simplified,
#             "tamil_text": tamil,
#             "audio_url": audio_url
#         }

#     except Exception as e:
#         return {"error": str(e)}

# # ----------- FILE TEXT EXTRACTION FUNCTION -----------

# def extract_text_from_file(file: UploadFile):
#     text = ""

#     if file.filename.endswith(".pdf"):
#         pdf = PdfReader(file.file)
#         for page in pdf.pages:
#             text += page.extract_text() or ""

#     elif file.filename.endswith(".docx"):
#         doc = docx.Document(file.file)
#         for para in doc.paragraphs:
#             text += para.text + "\n"

#     else:
#         text = file.file.read().decode("utf-8")

#     return text.strip()

# # ----------- FILE UPLOAD API -----------

# @app.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     try:
#         extracted_text = extract_text_from_file(file)

#         if not extracted_text:
#             return {"error": "No text extracted"}

#         # ⚠️ Limit text size (important)
#         extracted_text = extracted_text[:1000]

#         # ----------- AI PROCESSING -----------

#         chain = prompt | llm
#         response = chain.invoke({"text": extracted_text})

#         raw_output = response.content.strip()

#         try:
#             start = raw_output.find("{")
#             end = raw_output.rfind("}") + 1
#             clean_json = raw_output[start:end]

#             parsed = json.loads(clean_json)

#             simplified = parsed.get("simplified_text", "").strip()
#             tamil = parsed.get("tamil_text", "").strip()

#         except Exception:
#             simplified = raw_output
#             tamil = ""

#         # ----------- AUDIO -----------

#         audio_url = ""

#         if simplified:
#             file_hash = hashlib.md5(simplified.encode()).hexdigest()
#             file_path = f"audio/{file_hash}.mp3"

#             if not os.path.exists(file_path):
#                 tts = gTTS(text=simplified, lang='en')
#                 tts.save(file_path)

#             audio_url = f"http://127.0.0.1:8000/audio/{file_hash}.mp3"

#         return {
#             "simplified_text": simplified,
#             "tamil_text": tamil,
#             "audio_url": audio_url
#         }

#     except Exception as e:
#         return {"error": str(e)}

# # ----------- AUDIO ROUTE -----------

# @app.get("/audio/{filename}")
# async def get_audio(filename: str):
#     file_path = f"audio/{filename}"

#     if os.path.exists(file_path):
#         return FileResponse(file_path, media_type="audio/mpeg")

#     return {"error": "Audio not found"}

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from gtts import gTTS

from PyPDF2 import PdfReader
import docx

import json
import os
import hashlib

app = FastAPI()

# ----------- CORS -----------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------- CREATE AUDIO FOLDER -----------

os.makedirs("audio", exist_ok=True)

# ----------- REQUEST MODEL -----------

class TextRequest(BaseModel):
    text: str

# ----------- LLM MODEL -----------

llm = ChatOllama(
    model="mistral",
    temperature=0.1
)

# ----------- PROMPT -----------

prompt = ChatPromptTemplate.from_template("""
You are a legal document simplifier.

Your task is to simplify legal text into clear, simple English.

IMPORTANT RULES:

If the text is SHORT (1-2 sentences):
- Convert it into ONE simple sentence
- Maximum 12 words

If the text is LONG (document, multiple paragraphs):
- Extract ALL important information
- Do NOT summarize into one sentence
- Convert into multiple short bullet points

You MUST include:
• Important rules
• Deadlines
• Responsibilities
• Penalties
• Rights
• Important dates
• Required actions

Remove:
• Repeated sentences
• Legal jargon
• Unnecessary wording

Each bullet must:
- Be clear
- Be simple
- Be under 15 words

IMPORTANT:
Return ONLY valid JSON.

FORMAT:
{{
  "simplified_text": "..."
}}

TEXT:
{text}
""")
# ----------- TEXT INPUT API -----------

@app.post("/simplify/")
async def simplify_text(request: TextRequest):
    try:
        chain = prompt | llm
        response = chain.invoke({"text": request.text})

        raw_output = response.content.strip()

        try:
            start = raw_output.find("{")
            end = raw_output.rfind("}") + 1
            clean_json = raw_output[start:end]

            parsed = json.loads(clean_json)

            simplified = parsed.get("simplified_text", "").strip()

        except Exception:
            simplified = raw_output

        # ----------- AUDIO GENERATION -----------

        audio_url = ""

        if simplified:
            file_hash = hashlib.md5(simplified.encode()).hexdigest()
            file_path = f"audio/{file_hash}.mp3"

            if not os.path.exists(file_path):
                tts = gTTS(text=simplified, lang='en')
                tts.save(file_path)

            audio_url = f"http://127.0.0.1:8000/audio/{file_hash}.mp3"

        return {
            "simplified_text": simplified,
            "audio_url": audio_url
        }

    except Exception as e:
        return {"error": str(e)}

# ----------- FILE TEXT EXTRACTION -----------

def extract_text_from_file(file: UploadFile):
    text = ""

    if file.filename.endswith(".pdf"):
        pdf = PdfReader(file.file)
        for page in pdf.pages:
            text += page.extract_text() or ""

    elif file.filename.endswith(".docx"):
        doc = docx.Document(file.file)
        for para in doc.paragraphs:
            text += para.text + "\n"

    else:
        text = file.file.read().decode("utf-8")

    return text.strip()

# ----------- FILE UPLOAD API -----------

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        extracted_text = extract_text_from_file(file)

        if not extracted_text:
            return {"error": "No text extracted"}

        # Limit text size (important for LLM)
        extracted_text = extracted_text[:1000]

        chain = prompt | llm
        response = chain.invoke({"text": extracted_text})

        raw_output = response.content.strip()

        try:
            start = raw_output.find("{")
            end = raw_output.rfind("}") + 1
            clean_json = raw_output[start:end]

            parsed = json.loads(clean_json)

            simplified = parsed.get("simplified_text", "").strip()

        except Exception:
            simplified = raw_output

        # ----------- AUDIO GENERATION -----------

        audio_url = ""

        if simplified:
            file_hash = hashlib.md5(simplified.encode()).hexdigest()
            file_path = f"audio/{file_hash}.mp3"

            if not os.path.exists(file_path):
                tts = gTTS(text=simplified, lang='en')
                tts.save(file_path)

            audio_url = f"http://127.0.0.1:8000/audio/{file_hash}.mp3"

        return {
            "simplified_text": simplified,
            "audio_url": audio_url
        }

    except Exception as e:
        return {"error": str(e)}

# ----------- AUDIO ROUTE -----------

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    file_path = f"audio/{filename}"

    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg")

    return {"error": "Audio not found"}