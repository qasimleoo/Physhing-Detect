import re
import sqlite3

def analyze_url(url):

    score = 0
    reasons = []

    # ---------------- SAFE DOMAINS WHITELIST ----------------
    safe_domains = [
        "google.com",
        "microsoft.com",
        "amazon.com",
        "github.com",
        "youtube.com",
        "facebook.com",
        "twitter.com",
        "linkedin.com",
        "apple.com",
        "paypal.com",
        "bankofamerica.com",
        "chase.com",
        "netflix.com",
        "wikipedia.org",
        "stackoverflow.com"
    ]

    try:
        domain = url.split("//")[-1]
        domain = domain.split("/")[0]
        domain = domain.split("?")[0]
        domain = domain.lower()
        domain = domain.replace("www.", "")
        domain = domain.strip()

        for safe in safe_domains:
            if domain == safe or domain.endswith("." + safe):
                return {
                    "result": "safe",
                    "confidence": 95,
                    "reasons": [
                        "Domain is in trusted whitelist"
                    ]
                }
    except:
        pass

    # ---------------- DB CONNECTION ----------------
    conn = sqlite3.connect('phishing.db')
    cursor = conn.cursor()

    # ---------------- STEP 1: BLACKLIST CHECK ----------------
    cursor.execute("SELECT url FROM blacklist")
    blacklist = cursor.fetchall()

    for b in blacklist:
        if b[0] in url:
            conn.close()
            return {
                "result": "phishing",
                "confidence": 100,
                "reasons": ["URL found in blacklist database"]
            }

    # ---------------- STEP 2: IP ADDRESS CHECK ----------------
    if re.search(r'\d+\.\d+\.\d+\.\d+', url):
        score += 2
        reasons.append("IP address used in URL")

    # ---------------- STEP 3: URL LENGTH ----------------
    if len(url) > 100:
        score += 2
        reasons.append("Very long URL (>100 chars)")
    elif len(url) > 75:
        score += 1
        reasons.append("Long URL (>75 chars)")

    # ---------------- STEP 4: DOT COUNT ----------------
    if url.count('.') > 4:
        score += 1
        reasons.append("Too many dots in URL")

    # ---------------- STEP 5: HTTP CHECK ----------------
    if url.startswith("http://"):
        score += 2
        reasons.append("Unsecured HTTP protocol")

    # ---------------- STEP 6: DOMAIN EXTENSION ----------------
    suspicious_tlds = [".xyz", ".tk", ".ml", ".ga", ".cf"]
    for tld in suspicious_tlds:
        if tld in url:
            score += 2
            reasons.append(f"Suspicious domain: {tld}")

    # ---------------- STEP 7: KEYWORDS CHECK ----------------
    cursor.execute("SELECT keyword FROM phishing_keywords")
    keywords = cursor.fetchall()

    try:
        path = url.split("//")[-1].split("/", 1)
        url_path = path[1] if len(path) > 1 else ""
    except:
        url_path = url

    for k in keywords:
        if k[0].lower() in url_path.lower():
            score += 2
            reasons.append(f"Keyword found: {k[0]}")

    # ---------------- STEP 8: @ SYMBOL ----------------
    if "@" in url:
        score += 2
        reasons.append("Contains @ symbol")

    # ---------------- STEP 9: URL SHORTENERS ----------------
    shorteners = ["bit.ly", "tinyurl.com", "t.co"]
    for s in shorteners:
        if s in url:
            score += 4
            reasons.append("URL shortener detected")

    # ---------------- STEP 10: BRAND MISSPELLING ----------------
    brands = ["paypal", "google", "amazon", "microsoft"]
    for brand in brands:
        if brand in url.lower():
            if f"{brand}.com" not in url.lower():
                score += 3
                reasons.append(f"Brand spoofing: {brand}")

    # ---------------- STEP 11: DOUBLE SLASH ----------------
    path_part = url.split("//")[-1]
    if "//" in path_part:
        score += 1
        reasons.append("Double slashes in path")

    # ---------------- STEP 12: HYPHEN IN DOMAIN ----------------
    domain = url.split("//")[-1].split("/")[0]
    if "-" in domain:
        score += 1
        reasons.append("Hyphen in domain name")

    conn.close()

    # ---------------- FINAL SCORE CALCULATION ----------------
    if score <= 2:
        result = "safe"
        confidence = 90 - (score * 5)

    elif 3 <= score <= 5:
        result = "suspicious"
        confidence = 60 + (score * 5)

    else:
        result = "phishing"
        confidence = min(95, 80 + score * 2)

    return {
        "result": result,
        "confidence": confidence,
        "reasons": reasons
    }