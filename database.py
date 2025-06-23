import sqlite3
import os

def init_db():
    conn = sqlite3.connect("speech_data.db")  # ✅ Fixed typo in DB name
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS speech_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recognized_text TEXT NOT NULL,
            pdf_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_record(text, pdf_path=None):
    conn = sqlite3.connect("speech_data.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO speech_logs (recognized_text, pdf_path) VALUES (?, ?)",
        (text, pdf_path)
    )
    conn.commit()
    conn.close()

def fetch_all_record():
    conn = sqlite3.connect("speech_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM speech_logs ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
