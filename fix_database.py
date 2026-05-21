import sqlite3
from datetime import datetime

conn = sqlite3.connect('phishing.db')
cursor = conn.cursor()

# -------- DROP OLD USERS TABLE --------
cursor.execute("DROP TABLE IF EXISTS users")

# -------- CREATE NEW USERS TABLE WITH ALL COLUMNS --------
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT,
    password TEXT,
    role TEXT DEFAULT "user",
    created_at TEXT
)
''')

print("Users table fixed!")

# -------- INSERT ADMIN USER --------
cursor.execute(
    """INSERT OR IGNORE INTO users 
    (username, email, password, role, created_at) 
    VALUES (?, ?, ?, ?, ?)""",
    ("admin", "admin@phishguard.com", 
    "admin123", "admin", str(datetime.now()))
)

print("Admin user created!")

# -------- INSERT TEST USER --------
cursor.execute(
    """INSERT OR IGNORE INTO users 
    (username, email, password, role, created_at) 
    VALUES (?, ?, ?, ?, ?)""",
    ("tehreem", "tehreem@gmail.com", 
    "1234", "user", str(datetime.now()))
)

print("Test user created!")

conn.commit()
conn.close()

print("Database fixed successfully!")