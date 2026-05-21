import sqlite3
from datetime import datetime

conn = sqlite3.connect('phishing.db')
cursor = conn.cursor()

cursor.execute(
    """INSERT OR IGNORE INTO users 
    (username, email, password, role, created_at) 
    VALUES (?, ?, ?, ?, ?)""",
    ("admin", "admin@phishguard.com", 
    "admin123", "admin", str(datetime.now()))
)

conn.commit()
conn.close()

print("Admin user created successfully!")