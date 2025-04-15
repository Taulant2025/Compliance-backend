from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import openai
import os
from utils import extract_text_from_pdf

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize app
app = FastAPI()

# ✅ CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can later lock this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        content = await extract_text_from_pdf(file)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a compliance assistant for international trade contracts.",
                },
                {
                    "role": "user",
                    "content": f"Analyze this contract and tell me what's missing:\n\n{content}",
                },
            ],
            temperature=0.3,
        )

        return {"analysis": response.choices[0].message.content}

    except Exception as e:
        return {"error": str(e)}
