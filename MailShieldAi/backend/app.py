from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

from gemini_service import analyze_email

app = FastAPI(title="MailShield AI API")

# Allow Chrome Extension Requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EmailRequest(BaseModel):
    privacyMode: bool = False
    sender: str = ""
    subject: str = ""
    body: str = ""
    links: list = []


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "MailShield AI Backend Active"
    }


@app.post("/analyze")
def analyze(data: EmailRequest):

    email_data = {
        "sender": data.sender,
        "subject": data.subject,
        "body": data.body,
        "links": data.links
    }

    # Privacy Mode
    if data.privacyMode:
        email_data["body"] = "[REDACTED BY PRIVACY MODE]"

    gemini_result = analyze_email(email_data)

    risk_score = "Unknown"
    threat_type = "Unknown"
    explanation = ""

    try:

        # Remove markdown code blocks if Gemini adds them
        cleaned = gemini_result.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned.replace("```json", "", 1)

        if cleaned.startswith("```"):
            cleaned = cleaned.replace("```", "", 1)

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()

        result = json.loads(cleaned)

        risk_score = result.get(
            "risk_score",
            "Unknown"
        )

        threat_type = result.get(
            "threat_type",
            "Unknown"
        )

        explanation = result.get(
            "explanation",
            "No explanation provided."
        )

    except Exception as e:

        print("JSON Parse Error:", e)
        print("Gemini Response:", gemini_result)

        explanation = gemini_result

    return {
        "risk_score": risk_score,
        "threat_type": threat_type,
        "explanation": explanation
    }