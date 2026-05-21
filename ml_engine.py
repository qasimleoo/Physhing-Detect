import joblib
import numpy as np
import re
import pandas as pd

print("Loading ML Models...")

# ==========================================
# URL MODEL LOAD
# ==========================================
try:
    url_model = joblib.load('url_phishing_model.pkl')
    url_features = joblib.load('url_feature_names.pkl')
    url_ml_ready = True
    print("URL Model Loaded Successfully!")
except Exception as e:
    url_ml_ready = False
    print(f"URL Model Error: {e}")

# ==========================================
# EMAIL MODEL LOAD
# ==========================================
try:
    email_model = joblib.load('email_phishing_model.pkl')
    email_ml_ready = True
    print("Email Model Loaded Successfully!")
except Exception as e:
    email_ml_ready = False
    print(f"Email Model Error: {e}")


# ==========================================
# URL FEATURES EXTRACT
# ==========================================
def extract_url_features(url):

    features = {}

    # length_url
    features['length_url'] = len(url)

    # length_hostname
    try:
        hostname = url.split('//')[-1].split('/')[0]
        features['length_hostname'] = len(hostname)
    except:
        features['length_hostname'] = 0

    # ip
    features['ip'] = 1 if re.search(
        r'\d+\.\d+\.\d+\.\d+', url) else 0

    # nb_dots
    features['nb_dots'] = url.count('.')

    # nb_hyphens
    features['nb_hyphens'] = url.count('-')

    # nb_at
    features['nb_at'] = url.count('@')

    # nb_qm
    features['nb_qm'] = url.count('?')

    # nb_and
    features['nb_and'] = url.count('&')

    # nb_slash
    features['nb_slash'] = url.count('/')

    # nb_www
    features['nb_www'] = 1 if 'www' in url else 0

    # nb_com
    features['nb_com'] = 1 if '.com' in url else 0

    # nb_dslash
    features['nb_dslash'] = url.count('//')

    # http_in_path
    features['http_in_path'] = 1 if 'http' in url.split('//')[-1] else 0

    # https_token
    features['https_token'] = 1 if url.startswith('https') else 0

    # ratio_digits_url
    digits = sum(c.isdigit() for c in url)
    features['ratio_digits_url'] = digits / len(url) if len(url) > 0 else 0

    # ratio_digits_host
    try:
        host = url.split('//')[-1].split('/')[0]
        digits_host = sum(c.isdigit() for c in host)
        features['ratio_digits_host'] = digits_host / len(host) if len(host) > 0 else 0
    except:
        features['ratio_digits_host'] = 0

    # punycode
    features['punycode'] = 1 if 'xn--' in url else 0

    # port
    features['port'] = 1 if re.search(r':\d+', url) else 0

    # tld_in_path
    suspicious_tlds = ['.xyz', '.tk', '.ml', '.ga', '.cf']
    features['tld_in_path'] = 1 if any(
        tld in url for tld in suspicious_tlds) else 0

    # abnormal_subdomain
    features['abnormal_subdomain'] = 1 if url.count('.') > 3 else 0

    # nb_subdomains
    features['nb_subdomains'] = url.count('.')

    # prefix_suffix
    features['prefix_suffix'] = 1 if '-' in url.split('//')[-1].split('/')[0] else 0

    # shortening_service
    shorteners = ['bit.ly', 'tinyurl', 't.co', 'goo.gl']
    features['shortening_service'] = 1 if any(
        s in url for s in shorteners) else 0

    # nb_redirection
    features['nb_redirection'] = url.count('//')

    # phish_hints
    phish_words = ['login', 'verify', 'update',
                   'secure', 'account', 'bank',
                   'password', 'confirm']
    features['phish_hints'] = sum(
        1 for w in phish_words if w in url.lower())

    # domain_in_brand
    brands = ['paypal', 'google', 'amazon',
              'microsoft', 'apple', 'bank']
    features['domain_in_brand'] = 1 if any(
        b in url.lower() for b in brands) else 0

    # suspecious_tld
    features['suspecious_tld'] = 1 if any(
        tld in url for tld in suspicious_tlds) else 0

    # login_form
    features['login_form'] = 1 if 'login' in url.lower() else 0

    # external_favicon
    features['external_favicon'] = 0

    # iframe
    features['iframe'] = 0

    # popup_window
    features['popup_window'] = 0

    # domain_in_title
    features['domain_in_title'] = 0

    # domain_age
    features['domain_age'] = -1

    # web_traffic
    features['web_traffic'] = 0

    # page_rank
    features['page_rank'] = 0

    return features


# ==========================================
# ML URL ANALYZE
# ==========================================
def ml_analyze_url(url):

    if not url_ml_ready:
        return None

    try:
        # Features extract karein
        features = extract_url_features(url)

        # DataFrame banao
        features_df = pd.DataFrame([features])

        # Sirf woh features use karein jo training main the
        available = [
            f for f in url_features
            if f in features_df.columns
        ]
        features_df = features_df[available]

        # Missing columns fill karein
        for col in url_features:
            if col not in features_df.columns:
                features_df[col] = 0

        features_df = features_df[url_features]

        # Prediction
        prediction = url_model.predict(features_df)[0]
        probability = url_model.predict_proba(
            features_df)[0]

        confidence = int(max(probability) * 100)

        if prediction == 1:
            result = "phishing"
        else:
            result = "safe"

        return {
            "result": result,
            "confidence": confidence,
            "reasons": [
                f"ML Model Analysis Complete",
                f"Prediction: {result.upper()}",
                f"Confidence: {confidence}%",
                "Powered by Random Forest Classifier"
            ]
        }

    except Exception as e:
        print(f"ML URL Error: {e}")
        return None


# ==========================================
# ML EMAIL ANALYZE
# ==========================================
def ml_analyze_email(sender, subject, body):

    if not email_ml_ready:
        return None

    try:
        # Email text combine karein
        email_text = f"{subject} {body}"

        # Prediction
        prediction = email_model.predict(
            [email_text])[0]
        probability = email_model.predict_proba(
            [email_text])[0]

        confidence = int(max(probability) * 100)

        if prediction == 1:
            result = "phishing"
            risk_score = min(10,
                int(confidence / 10))
        else:
            result = "safe"
            risk_score = max(1,
                int((100 - confidence) / 10))

        return {
            "result": result,
            "confidence": confidence,
            "risk_score": risk_score,
            "flags": [
                f"ML Model: {result.upper()} detected",
                f"Confidence Level: {confidence}%",
                f"Risk Score: {risk_score}/10",
                "Powered by Naive Bayes Classifier"
            ],
            "highlights": []
        }

    except Exception as e:
        print(f"ML Email Error: {e}")
        return None