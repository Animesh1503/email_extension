MailShield AI

AI-Powered Email Threat Detection for Gmail

MailShield AI is a Chrome Extension that helps users identify phishing, scam, malware, impersonation, and credential theft emails directly inside Gmail. It combines rule-based security analysis with Google Gemini AI to provide intelligent threat detection, risk scoring, and easy-to-understand explanations before users interact with suspicious emails.

🚀 Features
🔍 Smart Email Analysis
Analyzes sender details
Scans email content
Checks suspicious keywords
Detects potentially dangerous links
🤖 AI-Powered Threat Detection
Uses Google Gemini AI
Identifies:
Phishing
Scam
Malware
Credential Theft
Impersonation
Safe Emails
📊 Risk Scoring System
Generates a risk score from 0–100
Categorizes emails as:
🟢 Safe
🟡 Medium Risk
🔴 High Risk
🛡 Privacy Mode
Redacts email body before sending data to AI
Helps protect sensitive information
📋 Threat Explanation
Provides a simple explanation of why an email is considered risky
Displays detected suspicious indicators
🎨 User-Friendly Interface
Chrome Extension popup UI
Risk badges
Progress bar visualization
Threat summary cards
🏗️ Tech Stack
Frontend
HTML
CSS
JavaScript
Chrome Extension Manifest V3
Backend
FastAPI
Python
AI Integration
Google Gemini API
Security Analysis
Rule-Based Detection Engine
AI Threat Classification
📂 Project Structure
MailShieldAI/
│
├── extension/
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.css
│   ├── popup.js
│   ├── content.js
│   └── background.js
│
├── backend/
│   ├── app.py
│   ├── analyzer.py
│   ├── gemini_service.py
│   ├── risk_scorer.py
│   ├── .env
│   └── requirements.txt
│
└── README.md
⚙️ Installation
1. Clone Repository
git clone https://github.com/yourusername/mailshield-ai.git
cd mailshield-ai
2. Install Backend Dependencies
pip install -r requirements.txt
3. Create Environment File

Create a .env file inside the backend folder:

GEMINI_API_KEY=YOUR_GEMINI_API_KEY
4. Start Backend Server
python -m uvicorn app:app --reload

Backend runs at:

http://127.0.0.1:8000
5. Load Chrome Extension
Open Chrome
Go to:
chrome://extensions
Enable Developer Mode
Click Load Unpacked
Select the extension folder
📖 How It Works
Step 1

User opens an email in Gmail.

Step 2

MailShield AI extracts:

Sender
Subject
Email Body
Links
Step 3

Rule-Based Engine checks for:

Suspicious keywords
URL shorteners
Multiple links
Credential requests
Suspicious sender patterns
Step 4

Gemini AI performs contextual threat analysis.

Step 5

Results are displayed:

Risk Score
Risk Level
Threat Type
Detected Risks
AI Explanation
📊 Example Output
{
  "risk_score": 78,
  "risk_level": "HIGH",
  "threat_type": "Phishing",
  "detected_risks": [
    "Suspicious keyword detected: verify",
    "Sensitive credential request detected"
  ],
  "explanation": "The email attempts to create urgency and asks the user to verify account credentials through a suspicious link."
}
🎯 Problem Statement

Email-based cyberattacks such as phishing, scams, credential theft, and malware distribution are becoming increasingly sophisticated, making it difficult for users to distinguish between legitimate and malicious emails. Many fraudulent emails bypass traditional spam filters and use deceptive tactics such as fake sender identities, suspicious links, and urgent messages to trick users into revealing sensitive information.

💡 Solution

MailShield AI provides real-time email threat analysis inside Gmail using a combination of rule-based detection and Google Gemini AI. The system evaluates email content, sender information, and links to generate a risk score, identify threat types, and explain potential dangers in simple language, helping users make safer decisions before interacting with suspicious emails.

🔮 Future Enhancements
Sender Reputation Analysis
URL Reputation Checking
Attachment Malware Detection
AI Email Summarization
Threat History Dashboard
Organization-wide Email Protection
Multi-language Support
Real-time Threat Intelligence Integration
