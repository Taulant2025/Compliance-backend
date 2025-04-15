# main.py
import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import openai
from utils import extract_text_from_pdf

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set your Vercel domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    content = await extract_text_from_pdf(file)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're a compliance assistant."},
            {"role": "user", "content": f"Analyze this document:\n\n{content}"},
        ],
        temperature=0.3
    )
    return {"analysis": response.choices[0].message.content}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))  # default to 10000
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
