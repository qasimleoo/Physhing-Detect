# 1. Project Preparation (Local Setup)

## Before deployment, the Flask project was structured properly:

# 2. Create Virtual Environment

A clean virtual environment was created to isolate dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# 3. Install Required Dependencies

Installed only project-specific libraries:

```bash
pip install flask numpy pandas scikit-learn scipy joblib gunicorn
```

---

# 4. Generate requirements.txt

A clean dependency file was created:

```bash
pip freeze > requirements.txt
```

Then manually cleaned to remove unnecessary/system packages.

---

# 5. Initialize Git Repository

```bash
git init
git add .
git commit -m "Initial commit - PhishGuard project"
```

---

# 6. Push Project to GitHub

Created a repository and pushed code:

```bash
git branch -M master
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin master
```

---

# 7. Connect GitHub to Render

On Render platform:

1. Selected **New Web Service**
2. Connected GitHub account
3. Selected PhishGuard repository
4. Render automatically detected Python project

---

# 8. Deployment Configuration on Render

## Build Command:

```bash
pip install -r requirements.txt
```

## Start Command:

```bash
gunicorn app:app
```

---

# 9. Major Deployment Issues & Fixes

## ❌ Issue 1: Wrong Python Version (Python 3.14)

- Render was using Python 3.14 by default
- ML libraries (NumPy, Pandas, Scikit-learn) failed

### ✅ Fix:

Created file:

```
.python-version
```

Content:

```
3.11.9
```

---

## ❌ Issue 2: Missing Gunicorn

- Deployment failed with:

```
gunicorn: command not found
```

### ✅ Fix:

Added to requirements.txt:

```
gunicorn==21.2.0
```

---

## ❌ Issue 3: NumPy & Pandas Source Build Problem

- Libraries were downloaded as `.tar.gz` (source builds)
- Caused slow installation

### Root Cause:

Python 3.14 incompatibility

### Fix:

Downgraded Python to 3.11.9

---

## ❌ Issue 4: Invalid / Conflicting Requirements

Earlier requirements included:

- incorrect package versions
- incompatible ML library versions

### Fix:

Cleaned requirements.txt to only include stable versions:

- Flask==3.0.3
- numpy==1.26.4
- pandas==2.2.2
- scikit-learn==1.4.2
- scipy==1.11.4
- joblib==1.3.2
- gunicorn==21.2.0

---

# 10. Final Successful Deployment Flow

After fixes:

1. Code pushed to GitHub
2. Render pulled latest repository
3. Python 3.11 environment activated
4. Dependencies installed successfully
5. Gunicorn started application
6. Flask app deployed successfully

---

# 🌐 Final Output

The application is now:

✔ Hosted on Render
✔ Accessible via public URL
✔ Running Flask backend with Gunicorn
✔ Fully functional ML-based phishing detection system
