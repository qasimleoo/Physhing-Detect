from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
from datetime import datetime

from ai_engine_email import analyze_email
from ai_engine import analyze_url

# train models import
from ml_engine import ml_analyze_url
from ml_engine import ml_analyze_email
import os

app = Flask(__name__)
app.secret_key = "phishguard_secret_key_2025"

port = int(os.environ.get("PORT", 5000))

# ---------------- DB INIT ----------------
def init_db():
    conn = sqlite3.connect('phishing.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT,
        password TEXT,
        role TEXT DEFAULT "user",
        created_at TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS login_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        timestamp TEXT,
        status TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        type TEXT,
        input TEXT,
        result TEXT,
        date TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS phishing_keywords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT,
        category TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS blacklist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()


# ================================================
# PAGE ROUTES
# ================================================

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print("======================")
        print("USERNAME:", username)
        print("PASSWORD:", password)

        conn = sqlite3.connect('phishing.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cursor.fetchone()

        print("USER FOUND:", user)
        print("======================")

        cursor.execute(
            "INSERT INTO login_logs (username, timestamp, status) VALUES (?, ?, ?)",
            (username, str(datetime.now()),
            "success" if user else "failed")
        )
        conn.commit()
        conn.close()

        if user:
            session['username'] = username
            session['role'] = user[4]
            return redirect('/dashboard')
        else:
            return render_template(
                'login.html',
                error="Invalid username or password"
            )

    return render_template('login.html')



# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Validation
        if not username or not email or not password:
            return render_template(
                'register.html',
                error="All fields are required"
            )

        conn = sqlite3.connect('phishing.db')
        cursor = conn.cursor()

        # Check if username exists
        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )
        existing = cursor.fetchone()

        if existing:
            conn.close()
            return render_template(
                'register.html',
                error="Username already exists!"
            )

        # Insert new user
        cursor.execute(
            """INSERT INTO users 
            (username, email, password, role, created_at) 
            VALUES (?, ?, ?, ?, ?)""",
            (username, email, password, 
            "user", str(datetime.now()))
        )

        conn.commit()
        conn.close()

        return render_template(
            'register.html',
            success="Account created! You can login now!"
        )

    return render_template('register.html')


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# ---------------- URL CHECKER PAGE ----------------
@app.route('/url_checker')
def url_checker():
    return render_template('url_checker.html')


# ---------------- CHECK URL ----------------
@app.route('/check-url', methods=['POST'])
def check_url():
    url = request.form['url']

    # Pehle ML try karein
    result = ml_analyze_url(url)

    # Agar ML fail ho toh Rules use karein
    if not result:
        result = analyze_url(url)

    if not isinstance(result, dict):
        return render_template(
            'url_checker.html',
            result="Error",
            confidence=0,
            reasons=["Invalid response"]
        )

    label = result.get("result", "unknown")
    confidence = result.get("confidence", 0)
    reasons = result.get("reasons", [])

    conn = sqlite3.connect('phishing.db')
    cursor = conn.cursor()

    username = session.get('username', 'guest')

    cursor.execute("""
        INSERT INTO logs (user, type, input, result, date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        "URL",
        url,
        f"{label} ({confidence}%)",
        str(datetime.now())
    ))

    conn.commit()
    conn.close()

    return render_template(
        'url_checker.html',
        result=label,
        confidence=confidence,
        reasons=reasons
    )

# ---------------- EMAIL SCANNER PAGE ----------------
@app.route('/email-scanner')
def email_scanner():
    return render_template('email_scanner.html')


# ---------------- SCAN EMAIL ----------------
@app.route('/scan-email', methods=['POST'])
def scan_email():
    sender = request.form['sender']
    subject = request.form['subject']
    body = request.form['body']

    # Pehle ML try karein
    result = ml_analyze_email(sender, subject, body)

    # Agar ML fail ho toh Rules use karein
    if not result:
        result = analyze_email(sender, subject, body)

    conn = sqlite3.connect('phishing.db')
    cursor = conn.cursor()

    username = session.get('username', 'guest')

    cursor.execute("""
        INSERT INTO logs (user, type, input, result, date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        "Email",
        sender,
        result.get("result", "unknown"),
        str(datetime.now())
    ))

    conn.commit()
    conn.close()

    return render_template(
        'email_scanner.html',
        result=result
    )


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():

    if 'username' not in session:
        return redirect('/login')

    conn = sqlite3.connect('phishing.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM logs")
    total_scans = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM logs WHERE result LIKE '%phishing%'"
    )
    phishing = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM logs WHERE result LIKE '%safe%'"
    )
    safe = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM logs WHERE result LIKE '%suspicious%'"
    )
    suspicious = cursor.fetchone()[0]

    cursor.execute(
        "SELECT * FROM logs ORDER BY id DESC LIMIT 10"
    )
    logs = cursor.fetchall()

    conn.close()

    return render_template(
        'dashboard.html',
        total_scans=total_scans,
        phishing=phishing,
        safe=safe,
        suspicious=suspicious,
        logs=logs,
        username=session.get('username')
    )


# ---------------- REPORT ----------------
@app.route('/report')
def report():
    return render_template('report.html')


# ---------------- REPORT DATA ----------------
@app.route('/report-data')
def report_data():
    conn = sqlite3.connect('phishing.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM logs ORDER BY date DESC"
    )
    rows = cursor.fetchall()
    conn.close()

    logs = []
    for row in rows:
        logs.append({
            "id": row[0],
            "user": row[1],
            "type": row[2],
            "input": row[3],
            "result": row[4],
            "date": row[5]
        })

    return jsonify({"logs": logs})


# ---------------- EDUCATION ----------------
@app.route('/education')
def education():
    return render_template('education.html')


# ---------------- ADMIN ----------------
@app.route('/admin')
def admin():

    if session.get('role') != 'admin':
        return redirect('/login')

    conn = sqlite3.connect('phishing.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM logs ORDER BY id DESC")
    logs = cursor.fetchall()

    cursor.execute(
        "SELECT COUNT(*) FROM logs WHERE result LIKE '%phishing%'"
    )
    threats = cursor.fetchone()[0]

    conn.close()

    return render_template(
        'admin.html',
        users=total_users,
        scans=len(logs),
        threats=threats,
        logs=logs
    )


# ---------------- ADD KEYWORD ----------------
@app.route('/add-keyword', methods=['POST'])
def add_keyword():
    keyword = request.form['keyword']
    category = request.form['category']

    conn = sqlite3.connect('phishing.db', timeout=10)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO phishing_keywords (keyword, category) VALUES (?, ?)",
            (keyword, category)
        )
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()
        conn.close()

    return redirect('/admin')


# ---------------- ADD URL ----------------
@app.route('/add-url', methods=['POST'])
def add_url():
    url = request.form['url']

    conn = sqlite3.connect('phishing.db', timeout=10)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO blacklist (url) VALUES (?)",
            (url,)
        )
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()
        conn.close()

    return redirect('/admin')


# ================================================
# API ROUTES
# ================================================

# ---------------- API: REGISTER ----------------
@app.route('/api/register', methods=['POST'])
def api_register():

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not password or not email:
        return jsonify({
            "success": False,
            "message": "All fields are required"
        })

    conn = sqlite3.connect('phishing.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    existing = cursor.fetchone()

    if existing:
        conn.close()
        return jsonify({
            "success": False,
            "message": "Username already exists"
        })

    cursor.execute(
        "INSERT INTO users (username, email, password, role, created_at) VALUES (?, ?, ?, ?, ?)",
        (username, email, password, "user", str(datetime.now()))
    )

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Registration successful"
    })


# ---------------- API: LOGIN ----------------
@app.route('/api/login', methods=['POST'])
def api_login():

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({
            "success": False,
            "message": "All fields are required"
        })

    conn = sqlite3.connect('phishing.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    user = cursor.fetchone()

    cursor.execute(
        "INSERT INTO login_logs (username, timestamp, status) VALUES (?, ?, ?)",
        (username, str(datetime.now()),
        "success" if user else "failed")
    )

    conn.commit()
    conn.close()

    if user:
        session['username'] = username
        session['role'] = user[4]

        return jsonify({
            "success": True,
            "message": "Login successful",
            "role": user[4]
        })
    else:
        return jsonify({
            "success": False,
            "message": "Invalid username or password"
        })


# ---------------- API: CHECK URL ----------------
@app.route('/api/check-url', methods=['POST'])
def api_check_url():

    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({
            "success": False,
            "message": "URL is required"
        })

    result = analyze_url(url)
    username = session.get('username', 'guest')

    conn = sqlite3.connect('phishing.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO logs (user, type, input, result, date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        "URL",
        url,
        result.get("result", "unknown"),
        str(datetime.now())
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "result": result.get("result"),
        "confidence": result.get("confidence"),
        "reasons": result.get("reasons")
    })


# ---------------- API: SCAN EMAIL ----------------
@app.route('/api/scan-email', methods=['POST'])
def api_scan_email():

    data = request.get_json()
    sender = data.get('sender')
    subject = data.get('subject')
    body = data.get('body')

    if not sender or not subject or not body:
        return jsonify({
            "success": False,
            "message": "All fields are required"
        })

    result = analyze_email(sender, subject, body)
    username = session.get('username', 'guest')

    conn = sqlite3.connect('phishing.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO logs (user, type, input, result, date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        "Email",
        sender,
        result.get("result", "unknown"),
        str(datetime.now())
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "result": result.get("result"),
        "risk_score": result.get("risk_score"),
        "flags": result.get("flags"),
        "highlights": result.get("highlights")
    })


# ---------------- API: SCAN HISTORY ----------------
@app.route('/api/scan-history')
def api_scan_history():

    conn = sqlite3.connect('phishing.db')
    cursor = conn.cursor()

    username = session.get('username', 'guest')

    cursor.execute(
        "SELECT * FROM logs WHERE user = ? ORDER BY id DESC LIMIT 20",
        (username,)
    )
    rows = cursor.fetchall()
    conn.close()

    logs = []
    for row in rows:
        logs.append({
            "id": row[0],
            "user": row[1],
            "type": row[2],
            "input": row[3],
            "result": row[4],
            "date": row[5]
        })

    return jsonify({
        "success": True,
        "logs": logs
    })


# ---------------- API: STATS ----------------
@app.route('/api/stats')
def api_stats():

    conn = sqlite3.connect('phishing.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM logs")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM logs WHERE result LIKE '%phishing%'"
    )
    phishing = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM logs WHERE result LIKE '%safe%'"
    )
    safe = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM logs WHERE result LIKE '%suspicious%'"
    )
    suspicious = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM logs WHERE type = 'URL'"
    )
    url_scans = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM logs WHERE type = 'Email'"
    )
    email_scans = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "success": True,
        "total": total,
        "phishing": phishing,
        "safe": safe,
        "suspicious": suspicious,
        "url_scans": url_scans,
        "email_scans": email_scans
    })


# ---------------- API: ADMIN ALL SCANS ----------------
@app.route('/api/admin/all-scans')
def api_admin_all_scans():

    conn = sqlite3.connect('phishing.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM logs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    logs = []
    for row in rows:
        logs.append({
            "id": row[0],
            "user": row[1],
            "type": row[2],
            "input": row[3],
            "result": row[4],
            "date": row[5]
        })

    return jsonify({
        "success": True,
        "logs": logs
    })


# ---------------- API: ADMIN ADD KEYWORD ----------------
@app.route('/api/admin/add-keyword', methods=['POST'])
def api_add_keyword():

    data = request.get_json()
    keyword = data.get('keyword')
    category = data.get('category')

    if not keyword or not category:
        return jsonify({
            "success": False,
            "message": "All fields are required"
        })

    conn = sqlite3.connect('phishing.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO phishing_keywords (keyword, category) VALUES (?, ?)",
        (keyword, category)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Keyword added successfully"
    })


# ---------------- API: ADMIN ADD BLACKLIST ----------------
@app.route('/api/admin/add-blacklist', methods=['POST'])
def api_add_blacklist():

    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({
            "success": False,
            "message": "URL is required"
        })

    conn = sqlite3.connect('phishing.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO blacklist (url) VALUES (?)",
        (url,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "URL added to blacklist successfully"
    })


# ================================================
# RUN APP - ALWAYS AT THE VERY BOTTOM
# ================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)


# added a new change