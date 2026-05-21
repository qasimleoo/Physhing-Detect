import sqlite3

conn = sqlite3.connect('phishing.db')
cursor = conn.cursor()

# -------- USERS TABLE --------
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

# -------- LOGIN LOGS TABLE --------
cursor.execute('''
CREATE TABLE IF NOT EXISTS login_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    timestamp TEXT,
    status TEXT
)
''')

# -------- LOGS TABLE --------
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

# -------- KEYWORDS TABLE --------
cursor.execute('''
CREATE TABLE IF NOT EXISTS phishing_keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT UNIQUE,
    category TEXT
)
''')

# -------- BLACKLIST TABLE --------
cursor.execute('''
CREATE TABLE IF NOT EXISTS blacklist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE
)
''')

conn.commit()

# -------- INSERT 50+ KEYWORDS --------
cursor.execute("DELETE FROM phishing_keywords")

keywords = [
    ("verify account", "urgency"),
    ("update password", "urgency"),
    ("login now", "urgency"),
    ("urgent action", "urgency"),
    ("act now", "urgency"),
    ("immediately", "urgency"),
    ("limited time", "urgency"),
    ("expire soon", "urgency"),
    ("24 hours", "urgency"),
    ("account suspended", "threat"),
    ("bank alert", "threat"),
    ("security alert", "threat"),
    ("unauthorized access", "threat"),
    ("fraud detected", "threat"),
    ("account locked", "threat"),
    ("account disabled", "threat"),
    ("permanently closed", "threat"),
    ("click here", "action"),
    ("click below", "action"),
    ("download attachment", "action"),
    ("open attachment", "action"),
    ("update now", "action"),
    ("confirm identity", "sensitive"),
    ("verify identity", "sensitive"),
    ("confirm account", "sensitive"),
    ("enter password", "sensitive"),
    ("social security", "sensitive"),
    ("credit card", "sensitive"),
    ("bank account", "sensitive"),
    ("login", "suspicious"),
    ("verify", "suspicious"),
    ("update", "suspicious"),
    ("secure", "suspicious"),
    ("account", "suspicious"),
    ("banking", "suspicious"),
    ("confirm", "suspicious"),
    ("signin", "suspicious"),
    ("password", "suspicious"),
    ("suspended", "threat"),
    ("warning", "threat"),
    ("dear customer", "generic"),
    ("dear user", "generic"),
    ("valued customer", "generic"),
    ("dear valued", "generic"),
    ("reset password", "action"),
    ("validate account", "action"),
    ("reactivate account", "action"),
    ("free gift", "urgency"),
    ("you have won", "urgency"),
    ("claim now", "urgency"),
    ("otp", "sensitive"),
    ("pin number", "sensitive")
]

cursor.executemany(
    "INSERT OR IGNORE INTO phishing_keywords "
    "(keyword, category) VALUES (?, ?)",
    keywords
)

# -------- INSERT 20+ BLACKLIST URLs --------
cursor.execute("DELETE FROM blacklist")

blacklist_urls = [
    ("http://fakebank.com",),
    ("http://login-secure.net",),
    ("http://verify-account.com",),
    ("http://paypal-alert.net",),
    ("http://192.168.1.1/login",),
    ("http://paypa1-secure.login-verify.xyz",),
    ("http://amaz0n.com-secure-login.tk",),
    ("http://bankofamerica.account-update.ml",),
    ("http://secure-banking-login.com@evil.com",),
    ("http://login-verify-account-secure.com",),
    ("http://banking-secure-verify.xyz",),
    ("http://account-update-required.com",),
    ("http://secure-paypal-login.tk",),
    ("http://google.com.evil-site.com",),
    ("http://microsoft-verify.ml",),
    ("http://amazon-security-alert.xyz",),
    ("http://bank-login-update.cf",),
    ("http://phishing-test-site.buzz",),
    ("http://steal-credentials.top",),
    ("http://fake-banking-portal.ga",),
]

cursor.executemany(
    "INSERT OR IGNORE INTO blacklist (url) VALUES (?)",
    blacklist_urls
)

conn.commit()
conn.close()

print("Database created successfully with all tables!")
print("50+ keywords inserted!")
print("20+ blacklist URLs inserted!")