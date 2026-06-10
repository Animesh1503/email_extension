# 🛡️ MailShield AI

### AI-Powered Email Threat Detection for Gmail

**Tagline:** Detect Suspicious Emails Before You Click.

---

## 📌 Problem Statement

Email remains one of the most common attack vectors for phishing, scams, credential theft, malware distribution, and impersonation attacks. Many users struggle to identify malicious emails because modern phishing attempts often mimic legitimate organizations and use convincing language. Existing email platforms may not provide sufficient real-time explanations about why an email is dangerous, leaving users vulnerable to cyber threats.

---

## 💡 Solution

MailShield AI is a Chrome Extension that analyzes Gmail emails in real time using a combination of:

* Rule-Based Threat Detection
* AI-Powered Analysis using Google Gemini
* Risk Scoring Engine
* Privacy Mode for secure analysis

The extension helps users understand whether an email is safe or potentially malicious by providing:

* Risk Score (0–100)
* Risk Level (Low / Medium / High)
* Threat Category
* Suspicious Indicators Detected
* AI-Generated Explanation

---

## 🚀 Features

### 🔍 Email Analysis

Analyzes sender information, email content, and embedded links.

### 🤖 AI Threat Detection

Uses Google Gemini AI to classify emails into:

* Safe
* Phishing
* Scam
* Malware
* Credential Theft
* Impersonation

### 📊 Risk Scoring System

Generates a numerical risk score and categorizes emails into:

* 🟢 Low Risk
* 🟡 Medium Risk
* 🔴 High Risk

### 🔐 Privacy Mode

Redacts email content before sending data to the AI model.

### 📋 Suspicious Indicator Detection

Detects:

* Urgency language
* Password requests
* OTP requests
* Suspicious sender patterns
* URL shorteners
* Excessive links

---

## 🏗️ Tech Stack

### Frontend

* HTML
* CSS
* JavaScript
* Chrome Extension Manifest V3

### Backend

* FastAPI
* Python

### AI Integration

* Google Gemini API

---

## 📂 Project Structure

MailShieldAI/

├── frontend/

│ ├── popup.html

│ ├── popup.css

│ ├── popup.js

│ ├── content.js

│ ├── background.js

│ └── manifest.json

│

├── backend/

│ ├── app.py

│ ├── analyzer.py

│ ├── gemini_service.py

│ ├── risk_scorer.py

│ ├── .env

│ └── requirements.txt

│

└── README.md

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/MailShieldAI.git
cd MailShieldAI
```

### 2. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Gemini API Key

Create a `.env` file inside the backend folder:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

### 4. Start FastAPI Backend

```bash
uvicorn app:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

### 5. Load Chrome Extension

1. Open Chrome
2. Go to chrome://extensions
3. Enable Developer Mode
4. Click Load Unpacked
5. Select the extension folder

---

## 🧪 How It Works

1. User opens an email in Gmail.
2. MailShield extracts sender, subject, body, and links.
3. Local rule-based engine calculates risk score.
4. Email is analyzed using Gemini AI.
5. Results are displayed in a clean dashboard showing:

   * Risk Score
   * Risk Level
   * Threat Type
   * Suspicious Indicators
   * AI Explanation

---

## 🔮 Future Improvements

* URL Reputation Checking
* Domain Verification
* Attachment Scanning
* Machine Learning Risk Models
* Threat History Dashboard
* Real-Time Gmail Banner Warnings
* Dark Mode Support
* Multi-Language Email Analysis

---

## 👩‍💻 Developed By

Prachi Mehta

Second Year Information Technology Student

KJ Somaiya Institute of Technology

---

## ⭐ Project Goal

To provide an intelligent and user-friendly email security assistant that helps users identify phishing and scam emails before they become victims of cyber attacks.
