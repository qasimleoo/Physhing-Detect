

import re
from ai_engine import analyze_url

def analyze_email(sender, subject, body):

    score = 0
    flags = []
    highlights = []

    sender = sender.lower()
    subject = subject.lower()
    body_lower = body.lower()

    # ---------------- STEP 1: SENDER ANALYSIS ----------------

    free_providers = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]

    if any(domain in sender for domain in free_providers):
        flags.append("Free email provider used")
        score += 1

    # random numbers in sender
    if re.search(r'\d{3,}', sender):
        flags.append("Numbers in sender identity")
        score += 1

    # ---------------- STEP 2: SUBJECT ANALYSIS ----------------

    urgency_words = ["urgent", "immediately", "verify", "alert", "important"]

    if any(word in subject for word in urgency_words):
        flags.append("Urgency words in subject")
        score += 1

    if subject.isupper():
        flags.append("ALL CAPS subject")
        score += 1

    # ---------------- STEP 3: BODY ANALYSIS ----------------

    body_urgency = ["urgent", "immediately", "act now", "verify", "suspended"]
    sensitive_words = ["password", "otp", "bank", "account", "credit card"]
    threat_words = ["blocked", "suspended", "closed", "penalty"]

    # urgency keywords
    for word in body_urgency:
        if word in body_lower:
            flags.append(f"Urgency word: {word}")
            score += 1
            highlights.append(word)

    # sensitive data request
    for word in sensitive_words:
        if word in body_lower:
            flags.append(f"Sensitive request: {word}")
            score += 2
            highlights.append(word)

    # threat language
    for word in threat_words:
        if word in body_lower:
            flags.append(f"Threat word: {word}")
            score += 2
            highlights.append(word)

    # click here detection
    if "click here" in body_lower:
        flags.append("Call-to-action detected")
        score += 1
        highlights.append("click here")

    # ---------------- URLs INSIDE EMAIL ----------------

    urls = re.findall(r'(https?://\S+)', body)

    for url in urls:
        url_result = analyze_url(url)
        if url_result.get("result") == "phishing":
            flags.append(f"Phishing URL detected: {url}")
            score += 3

    # ---------------- EXCLAMATION MARKS ----------------

    if body.count("!") > 3:
        flags.append("Too many exclamation marks")
        score += 1

    # ---------------- MISSPELLING CHECK (basic) ----------------

    misspellings = ["accout", "verifiy", "securty", "logiin"]

    for word in misspellings:
        if word in body_lower:
            flags.append(f"Misspelling detected: {word}")
            score += 1
            highlights.append(word)

    # ---------------- GENERIC GREETING ----------------

    if "dear user" in body_lower or "dear customer" in body_lower:
        flags.append("Generic greeting used")
        score += 1

    # ---------------- STEP 4: RISK SCORE (1–10) ----------------

    risk_score = min(10, score)

    # ---------------- STEP 5: FINAL RESULT ----------------

    if risk_score <= 3:
        result = "safe"
    elif risk_score <= 6:
        result = "suspicious"
    else:
        result = "phishing"

    return {
        "result": result,
        "risk_score": risk_score,
        "flags": flags,
        "highlights": highlights
    }