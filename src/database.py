import sqlite3
from datetime import datetime

DB_NAME = "risk_analysis.db"


def get_connection():
    return sqlite3.connect(
        DB_NAME,
        check_same_thread=False
    )


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS risk_analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region TEXT NOT NULL,
            risk_score REAL NOT NULL,
            confidence_level TEXT NOT NULL,
            executive_summary TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS critical_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region TEXT NOT NULL,
            risk_score REAL NOT NULL,
            executive_summary TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_analysis(
    region,
    risk_score,
    confidence_level,
    executive_summary
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO risk_analyses (
            region,
            risk_score,
            confidence_level,
            executive_summary,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        region,
        risk_score,
        confidence_level,
        executive_summary,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def save_critical_alert(
    region,
    risk_score,
    executive_summary
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO critical_alerts (
            region,
            risk_score,
            executive_summary,
            timestamp
        )
        VALUES (?, ?, ?, ?)
    """, (
        region,
        risk_score,
        executive_summary,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_history(limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT region, risk_score, confidence_level, executive_summary, timestamp
        FROM risk_analyses
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_critical_alerts(limit=20):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT region, risk_score, executive_summary, timestamp
        FROM critical_alerts
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return rows


init_db()