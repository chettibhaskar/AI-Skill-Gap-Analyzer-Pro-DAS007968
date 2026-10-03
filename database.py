import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('analysis_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  job_role TEXT,
                  score INTEGER,
                  matched TEXT,
                  missing TEXT,
                  date TEXT)''')
    conn.commit()
    conn.close()

def save_analysis(job_role, score, matched, missing):
    conn = sqlite3.connect('analysis_history.db')
    c = conn.cursor()
    c.execute("INSERT INTO history (job_role, score, matched, missing, date) VALUES (?,?,?,?,?)",
              (job_role, score, str(matched), str(missing), datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect('analysis_history.db')
    c = conn.cursor()
    c.execute("SELECT * FROM history ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return data

init_db()