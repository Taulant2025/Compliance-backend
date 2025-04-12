from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from utils import extract_text_from_pdf
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow frontend (we'll hook React later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to your frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are supported at the moment."}

    content = await extract_text_from_pdf(file)

    prompt = f"""
You are a compliance analyst. Read this contract and identify missing or weak clauses related to:
1. Sanctions
2. Force majeure
3. Payment terms
4. Incoterms
5. Dispute resolution
Give a summary in bullet points.
Contract:
{content}
"""

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a legal compliance expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return {
        "analysis": response["choices"][0]["message"]["content"]
    }
