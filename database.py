"""
HealthPulse AI  - Database layer (SQLite)
Stores vitals history, medication reminders, and chat logs for the dashboard.
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "HealthPulse .db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS vitals_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_date TEXT NOT NULL,
            glucose REAL,
            bmi REAL,
            blood_pressure REAL,
            risk_score REAL,
            risk_label TEXT,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            med_name TEXT NOT NULL,
            reminder_time TEXT NOT NULL,
            frequency TEXT NOT NULL,
            active INTEGER DEFAULT 1,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reminder_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reminder_id INTEGER NOT NULL,
            log_date TEXT NOT NULL,
            taken INTEGER NOT NULL,
            FOREIGN KEY (reminder_id) REFERENCES reminders (id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_vitals_entry(glucose, bmi, blood_pressure, risk_score, risk_label):
    conn = get_connection()
    conn.execute(
        """INSERT INTO vitals_log (entry_date, glucose, bmi, blood_pressure, risk_score, risk_label, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (datetime.now().strftime("%Y-%m-%d"), glucose, bmi, blood_pressure,
         risk_score, risk_label, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_vitals_history(limit=30):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM vitals_log ORDER BY created_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in reversed(rows)]


def add_reminder(med_name, reminder_time, frequency):
    conn = get_connection()
    conn.execute(
        "INSERT INTO reminders (med_name, reminder_time, frequency, created_at) VALUES (?, ?, ?, ?)",
        (med_name, reminder_time, frequency, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_reminders():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM reminders WHERE active = 1 ORDER BY reminder_time"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mark_reminder_taken(reminder_id, taken=1):
    conn = get_connection()
    today = datetime.now().strftime("%Y-%m-%d")
    existing = conn.execute(
        "SELECT id FROM reminder_logs WHERE reminder_id = ? AND log_date = ?",
        (reminder_id, today)
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE reminder_logs SET taken = ? WHERE id = ?", (taken, existing["id"])
        )
    else:
        conn.execute(
            "INSERT INTO reminder_logs (reminder_id, log_date, taken) VALUES (?, ?, ?)",
            (reminder_id, today, taken)
        )
    conn.commit()
    conn.close()


def get_adherence_stats():
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) as c FROM reminder_logs").fetchone()["c"]
    taken = conn.execute("SELECT COUNT(*) as c FROM reminder_logs WHERE taken = 1").fetchone()["c"]
    conn.close()
    if total == 0:
        return {"taken": 0, "total": 0, "percentage": 100}
    return {"taken": taken, "total": total, "percentage": round((taken / total) * 100)}


def log_chat(sender, message):
    conn = get_connection()
    conn.execute(
        "INSERT INTO chat_history (sender, message, timestamp) VALUES (?, ?, ?)",
        (sender, message, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_chat_history(limit=50):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM chat_history ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in reversed(rows)]
