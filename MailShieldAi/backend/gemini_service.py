from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def analyze_email(email_data):

    prompt = f"""
You are a cybersecurity expert specializing in phishing and email threat detection.

Analyze the following email.

Sender:
{email_data.get('sender', '')}

Subject:
{email_data.get('subject', '')}

Body:
{email_data.get('body', '')}

Links:
{email_data.get('links', [])}

Return ONLY valid JSON.

Example:

{{
    "risk_score": 85,
    "threat_type": "Phishing",
    "explanation": "The sender domain appears suspicious and the email contains urgency language and potentially deceptive links."
}}

Rules:
- risk_score must be a number from 0 to 100
- threat_type must be one of:
  Safe
  Phishing
  Scam
  Malware
  Credential Theft
  Impersonation
- explanation must be under 100 words
- Return ONLY JSON
- Do not use markdown
- Do not use code blocks
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"""{{
            "risk_score": 0,
            "threat_type": "Error",
            "explanation": "Gemini API Error: {str(e)}"
        }}"""