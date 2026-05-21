import sqlite3

conn = sqlite3.connect('phishing.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS phishing_keywords")

cursor.execute('''
CREATE TABLE phishing_keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT UNIQUE,
    category TEXT
)
''')

keywords = [
    ("login", "suspicious"),
    ("verify", "suspicious"),
    ("update", "suspicious"),
    ("secure", "suspicious"),
    ("account", "suspicious"),
    ("banking", "suspicious"),
    ("confirm", "suspicious"),
    ("signin", "suspicious"),
    ("password", "suspicious"),
    ("bank", "suspicious"),
    ("alert", "urgency"),
    ("urgent", "urgency"),
    ("suspended", "threat"),
    ("blocked", "threat"),
    ("limited", "urgency"),
    ("expire", "urgency"),
    ("click", "action"),
    ("pay", "suspicious"),
    ("card", "suspicious"),
    ("credit", "suspicious"),
    ("transfer", "suspicious"),
    ("otp", "sensitive"),
    ("security", "suspicious"),
    ("reset", "suspicious"),
    ("recover", "suspicious"),
    ("unlock", "suspicious"),
    ("validate", "suspicious"),
    ("payment", "suspicious"),
    ("billing", "suspicious"),
    ("support", "suspicious"),
]

cursor.executemany(
    "INSERT OR IGNORE INTO phishing_keywords (keyword, category) VALUES (?, ?)",
    keywords
)

conn.commit()
conn.close()

print("Done! Keywords added successfully!")