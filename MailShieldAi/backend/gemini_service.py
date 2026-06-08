from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def analyze_email(email_data):
    sender = email_data.get("sender", "")
    subject = email_data.get("subject", "")
    body = email_data.get("body", "")
    links = email_data.get("links", []) or []

    formatted_links = "\n".join(str(link) for link in links)
    prompt = f"""
You are a cybersecurity expert specializing in phishing and email threat detection.

Analyze the following email and return ONLY valid JSON.

Sender:
{sender}

Subject:
{subject}

Body:
{body}

Links:
{formatted_links}

Return a JSON object with these fields:
- risk_score: number between 0 and 100
- threat_type: one of Safe, Phishing, Scam, Malware, Credential Theft, Impersonation
- confidence: number between 0 and 100
- explanation: string under 100 words

Example:
{{
    "risk_score": 85,
    "threat_type": "Phishing",
    "confidence": 92,
    "explanation": "The sender domain appears suspicious and the email contains urgency language and potentially deceptive links."
}}

Rules:
- Return ONLY valid JSON
- Do not use markdown
- Do not use code blocks
- Do not include any extra keys
"""
    try:
        # Debug: log truncated prompt to help tracing reused responses
        print("\n========== GEMINI PROMPT ==========")
        try:
            print(prompt[:1000])
        except Exception:
            print("(prompt too large to display)")
        print("===================================")

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
        )

        # Log full Gemini response for debugging
        try:
            print("\n========== GEMINI RESPONSE ==========")
            print(response.text)
            print("=====================================")
        except Exception:
            print("(response too large to display)")

        # Return raw text from Gemini (caller is responsible for parsing)
        return response.text

    except Exception as e:
        # Log error server-side
        print("Gemini API error:", str(e))
        return '{"risk_score": 0, "threat_type": "Error", "confidence": 0, "explanation": "Gemini API Error"}'
