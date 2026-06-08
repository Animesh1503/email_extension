import re
from urllib.parse import urlparse

TRUSTED_DOMAINS = {
    "google.com",
    "amazon.com",
    "amazon.in",
    "microsoft.com",
    "github.com",
    "linkedin.com",
    "paypal.com",
    "apple.com",
}

SUSPICIOUS_LOOKALIKE_DOMAINS = {
    "paypai.com",
    "arnazon.com",
    "g00gle.com",
    "micr0soft.com",
}

URL_SHORTENERS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
}

SUSPICIOUS_TLDS = {"xyz", "top", "click", "shop"}

KEYWORD_WEIGHTS = {
    "password": 20,
    "otp": 20,
    "one time password": 20,
    "click here": 15,
    "urgent": 5,
    "login": 5,
    "verify": 10,
    "account suspended": 20,
    "confirm your identity": 15,
    "update your account": 15,
    "billing": 10,
    "security alert": 10,
    "unusual activity": 10,
}

CREDENTIAL_KEYWORDS = {
    "password",
    "otp",
    "one time password",
    "login",
    "verify",
    "credentials",
    "account suspended",
    "confirm your identity",
    "update your account",
}

DOMAIN_EXTRACTOR = re.compile(r"<([^>]+)>")
WORD_BOUNDARY = re.compile(r"\b")
IP_ADDRESS_RE = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")


def _extract_sender_domain(sender: str) -> str:
    sender = (sender or "").strip()
    if not sender:
        return ""

    match = DOMAIN_EXTRACTOR.search(sender)
    if match:
        sender = match.group(1)

    if "@" in sender:
        sender = sender.split("@")[-1]

    sender = sender.lower().strip().strip(".")
    if ":" in sender:
        sender = sender.split(":")[0]
    return sender


def _normalize_domain(domain: str) -> str:
    domain = domain.lower().strip().strip(".")
    if ":" in domain:
        domain = domain.split(":")[0]
    return domain


def _is_trusted_domain(domain: str) -> bool:
    normalized = _normalize_domain(domain)
    if not normalized:
        return False
    return any(
        normalized == trusted or normalized.endswith(f".{trusted}")
        for trusted in TRUSTED_DOMAINS
    )


def _is_suspicious_lookalike_domain(domain: str) -> bool:
    normalized = _normalize_domain(domain)
    return normalized in SUSPICIOUS_LOOKALIKE_DOMAINS


def _build_keyword_pattern(keyword: str) -> re.Pattern:
    token_list = keyword.split()
    escaped_tokens = [re.escape(token) for token in token_list]
    pattern = r"\b" + r"\s+".join(escaped_tokens) + r"\b"
    return re.compile(pattern, flags=re.IGNORECASE)


def _find_weighted_keywords(text: str) -> tuple[int, list[str], bool]:
    score = 0
    detected = []
    credential_request = False
    normalized_text = text.lower()

    for keyword, weight in KEYWORD_WEIGHTS.items():
        pattern = _build_keyword_pattern(keyword)
        matches = pattern.findall(normalized_text)
        if not matches:
            continue

        occurrence_count = len(matches)
        score += weight * occurrence_count
        detected.append(f"Keyword '{keyword}' found {occurrence_count} time(s)")

        if keyword in CREDENTIAL_KEYWORDS:
            credential_request = True

    if not credential_request:
        for credential_keyword in CREDENTIAL_KEYWORDS:
            pattern = _build_keyword_pattern(credential_keyword)
            if pattern.search(normalized_text):
                credential_request = True
                break

    return score, detected, credential_request


def _is_ip_address(value: str) -> bool:
    return bool(IP_ADDRESS_RE.match(value))


def _analyze_link(url: str, sender_domain: str) -> tuple[int, list[str], bool, bool]:
    score = 0
    detected = []
    suspicious_link = False
    suspicious_domain_found = False

    raw_url = (url or "").strip()
    if not raw_url:
        return score, detected, suspicious_link, suspicious_domain_found

    if not raw_url.lower().startswith(("http://", "https://")):
        raw_url = "http://" + raw_url

    try:
        parsed = urlparse(raw_url)
        host = parsed.hostname or ""
        host = host.lower().strip().strip(".")
    except Exception:
        return score, detected, suspicious_link, suspicious_domain_found

    if not host:
        return score, detected, suspicious_link, suspicious_domain_found

    if _is_ip_address(host):
        score += 25
        detected.append(f"URL uses raw IP address: {url}")
        suspicious_link = True

    if any(host == shortener or host.endswith(f".{shortener}") for shortener in URL_SHORTENERS):
        score += 20
        detected.append(f"URL shortener detected: {host}")
        suspicious_link = True

    normalized_host = _normalize_domain(host)
    if _is_suspicious_lookalike_domain(normalized_host):
        score += 35
        detected.append(f"Lookalike domain detected: {normalized_host}")
        suspicious_link = True
        suspicious_domain_found = True

    tld = normalized_host.split('.')[-1] if '.' in normalized_host else ""
    if tld in SUSPICIOUS_TLDS:
        score += 15
        detected.append(f"Suspicious top-level domain: .{tld}")
        suspicious_link = True

    if sender_domain and normalized_host and sender_domain != normalized_host:
        if normalized_host.endswith(sender_domain) or sender_domain.endswith(normalized_host):
            # Do not penalize legitimate subdomain relationships too heavily.
            pass

    return score, detected, suspicious_link, suspicious_domain_found


def analyze_email(email_data: dict) -> dict:
    sender = email_data.get("sender", "")
    subject = email_data.get("subject", "")
    body = email_data.get("body", "")
    links = email_data.get("links", []) or []

    sender_domain = _extract_sender_domain(sender)
    trusted_sender = _is_trusted_domain(sender_domain)

    text_to_analyze = f"{subject}\n{body}"
    text_score, keyword_risks, credential_request = _find_weighted_keywords(text_to_analyze)

    link_score = 0
    link_risks = []
    suspicious_link_found = False
    suspicious_domain_found = False

    for url in links:
        score, detected, suspicious_link, suspicious_domain = _analyze_link(url, sender_domain)
        link_score += score
        link_risks.extend(detected)
        suspicious_link_found = suspicious_link_found or suspicious_link
        suspicious_domain_found = suspicious_domain_found or suspicious_domain

    raw_sender_domain = sender_domain.lower().strip()
    sender_domain_risk = 0
    sender_risks = []
    if raw_sender_domain and _is_suspicious_lookalike_domain(raw_sender_domain):
        sender_domain_risk += 35
        sender_risks.append(f"Suspicious sender domain detected: {raw_sender_domain}")

    base_score = text_score + link_score + sender_domain_risk
    if trusted_sender:
        base_score = max(0, base_score - 25)

    detected_risks = keyword_risks + link_risks + sender_risks
    detected_risks = list(dict.fromkeys(detected_risks))

    forced_low = False
    explanation = ""
    if trusted_sender and not suspicious_link_found and not credential_request:
        forced_low = True
        base_score = min(base_score, 10)
        explanation = (
            "Trusted sender detected, no suspicious links were found, "
            "and the message does not request credentials. Risk is forced to LOW."
        )
    else:
        if not detected_risks:
            explanation = "No strong phishing indicators were detected by the rule engine."
        else:
            explanation = "Rule-based analysis identified the following indicators: " + "; ".join(detected_risks)

    capped_score = min(100, max(0, int(base_score)))

    return {
        "rule_score": capped_score,
        "detected_risks": detected_risks,
        "explanation": explanation,
        "trusted_sender": trusted_sender,
        "safe_email": forced_low,
        "credential_request": credential_request,
        "suspicious_links": suspicious_link_found,
        "sender_domain": sender_domain,
    }


def get_risk_level(score: int) -> str:
    if score <= 33:
        return "LOW"
    if score <= 66:
        return "MEDIUM"
    return "HIGH"
