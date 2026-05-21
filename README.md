# FYP---ohishing-detection

# PhishGuard - AI Based Phishing Detection System

## Developer
- Name: Tehreem Fatima
- Degree: BS Information Technology
- Semester: 8th
- Year: 2026

## Project Overview
An AI-powered phishing detection system for 
online banking that detects suspicious URLs 
and phishing emails using Rule-Based Expert System.

## Tech Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python (Flask)
- Database: SQLite
- AI: Rule-Based Expert System

## Features
1. URL Phishing Detection
2. Email Phishing Scanner
3. User Dashboard
4. Admin Panel
5. Education and Awareness Page
6. Report and Analytics with Charts
7. Interactive Quiz
8. User Registration and Login

## How to Run

### Step 1: Install Flask
pip install flask

### Step 2: Setup Database
python fix_db_keywords.py

### Step 3: Create Admin User
python create_admin.py

### Step 4: Run Application
python app.py

### Step 5: Open Browser
http://127.0.0.1:5000

## Login Credentials
### Admin
- Username: admin
- Password: admin123

### Test User
- Username: tehreem
- Password: 1234

## Project Structure
phishing-detection-project/
|-- static/
|   |-- css/
|   |   |-- style.css
|   |   |-- dashboard.css
|   |   |-- url.css
|   |   |-- email.css
|   |   |-- login.css
|   |   |-- report.css
|   |   |-- admin.css
|   |   |-- education.css
|   |-- js/
|   |   |-- urlChecker.js
|   |   |-- emailScanner.js
|   |   |-- loginValidator.js
|   |   |-- dashboard.js
|   |   |-- report.js
|   |   |-- education.js
|   |   |-- admin.js
|   |-- images/
|-- templates/
|   |-- index.html
|   |-- login.html
|   |-- register.html
|   |-- dashboard.html
|   |-- url_checker.html
|   |-- email_scanner.html
|   |-- report.html
|   |-- education.html
|   |-- admin.html
|   |-- navbar.html
|-- app.py
|-- ai_engine.py
|-- ai_engine_email.py
|-- database.py
|-- phishing.db
|-- README.md

## AI Engine Details
This system uses a Rule-Based Expert System 
which is a classical form of Artificial Intelligence.

The AI engine works by using:
- Pattern Recognition: regex-based URL analysis
- Natural Language Processing: keyword detection
- Scoring Algorithm: weighted multi-factor assessment
- Knowledge Base: database of known phishing patterns

## URL Detection Rules (12 Rules)
1. IP address in URL (+2)
2. URL length check (+1 or +2)
3. Subdomain count (+1)
4. HTTP vs HTTPS (+2)
5. Suspicious extensions (+2)
6. Keyword detection (+2)
7. @ symbol detection (+2)
8. URL shortener detection (+4)
9. Brand misspelling (+3)
10. Double slash detection (+1)
11. Hyphen in domain (+1)
12. Blacklist check (instant PHISHING)

## Score to Result
- 0 to 2: SAFE
- 3 to 5: SUSPICIOUS
- 6 or more: PHISHING

## Email Detection Rules
1. Free email provider check
2. Numbers in sender name
3. Urgency words in subject
4. ALL CAPS subject
5. Urgency keywords in body
6. Sensitive data requests
7. Threat language
8. Action phrases
9. URL analysis in email
10. Exclamation marks
11. Misspelling detection
12. Generic greetings

## Risk Score Scale
- 0 to 3: SAFE
- 4 to 6: SUSPICIOUS
- 7 to 10: PHISHING



## AI Engine Details

### Hybrid Approach:
1. Machine Learning Layer:
   - URL Detection: Random Forest Classifier
     Trained on 11,430 URLs
     Accuracy: 95%+
   
   - Email Detection: Naive Bayes Classifier
     Trained on 5,572 Emails
     Accuracy: 97%+

2. Rule-Based Backup Layer:
   - If ML fails, Expert System takes over
   - 12 detection rules for URLs
   - 12 detection rules for Emails# Physhing-Detect
