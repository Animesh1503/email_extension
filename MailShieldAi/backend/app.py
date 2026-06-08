from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

from analyzer import analyze_email as analyze_rule_email, get_risk_level
from gemini_service import analyze_email as analyze_gemini_email

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
    links: list[str] = []


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
        "links": data.links,
    }

    if data.privacyMode:
        email_data["body"] = "[REDACTED BY PRIVACY MODE]"

    # Debug: log incoming email for reproducible tracing
    print("\n===== NEW ANALYSIS =====")
    print("Sender:", email_data["sender"])
    print("Subject:", email_data["subject"])
    print("Body Preview:", (email_data["body"] or "")[:300])

    rule_result = analyze_rule_email(email_data)

    # Additional debug print of the full email before calling Gemini
    print("\n========== NEW EMAIL ==========")
    print("Sender:", email_data.get("sender"))
    print("Subject:", email_data.get("subject"))
    print("Body:", (email_data.get("body") or "")[:200])
    print("================================")

    # Call Gemini for additional signal; gemini_service will log the prompt and response
    gemini_result = analyze_gemini_email(email_data)

    gemini_score = 0
    gemini_confidence = 0
    gemini_threat_type = "Unknown"
    gemini_explanation = ""

    try:
        cleaned = gemini_result.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned.replace("```json", "", 1)
        if cleaned.startswith("```"):
            cleaned = cleaned.replace("```", "", 1)
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        parsed = json.loads(cleaned)
        gemini_score = int(parsed.get("risk_score", 0) or 0)
        gemini_threat_type = parsed.get("threat_type", "Unknown")
        gemini_confidence = int(parsed.get("confidence", 0) or 0)
        gemini_explanation = parsed.get("explanation", "")

    except Exception as e:
        # Log detailed error server-side but do not expose internal API errors to extension UI
        print("Gemini parsing/error:", str(e))
        print("Gemini raw response:", gemini_result)

        gemini_score = 0
        gemini_threat_type = "Error"
        gemini_confidence = 0
        # Provide a user-friendly, non-sensitive explanation
        gemini_explanation = "External analysis unavailable; showing rule-based results."

    rule_score = int(rule_result.get("rule_score", 0) or 0)
    final_score = round((rule_score * 0.6) + (gemini_score * 0.4))

    # If the rule engine marks the message as explicitly safe, force low risk and use rule explanation.
    if rule_result.get("safe_email"):
        final_score = min(final_score, 15)
        risk_level = "LOW"
        threat_type = "Safe"
        explanation = rule_result.get("explanation", "Trusted sender with no suspicious indicators.")
        gemini_confidence = max(gemini_confidence, 80)
    else:
        # Prefer Gemini explanation only when Gemini reports sufficient confidence.
        GEMINI_CONFIDENCE_THRESHOLD = 60

        risk_level = get_risk_level(final_score)

        if gemini_threat_type != "Error" and gemini_confidence >= GEMINI_CONFIDENCE_THRESHOLD:
            threat_type = gemini_threat_type or "Unknown"
            explanation = gemini_explanation or rule_result.get("explanation", "No explanation provided.")
        else:
            # Use rule-based explanation if Gemini is unavailable or not confident enough.
            threat_type = "Rule-Based"
            explanation = rule_result.get("explanation", gemini_explanation or "No explanation provided.")

    return {
        "risk_score": final_score,
        "risk_level": risk_level,
        "threat_type": threat_type,
        "confidence": gemini_confidence,
        "detected_risks": rule_result.get("detected_risks", []),
        "explanation": explanation,
    }
