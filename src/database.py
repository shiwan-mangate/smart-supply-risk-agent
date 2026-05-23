import psycopg
from src.config import DATABASE_URL


def get_connection():
    return psycopg.connect(DATABASE_URL)


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Existing analysis history
            cur.execute("""
                CREATE TABLE IF NOT EXISTS risk_analyses (
                    id SERIAL PRIMARY KEY,
                    region TEXT NOT NULL,
                    risk_score INTEGER NOT NULL,
                    confidence_level TEXT NOT NULL,
                    executive_summary TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Existing critical alerts
            cur.execute("""
                CREATE TABLE IF NOT EXISTS critical_alerts (
                    id SERIAL PRIMARY KEY,
                    region TEXT NOT NULL,
                    risk_score INTEGER NOT NULL,
                    executive_summary TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # NEW vector memory table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS agent_memories (
                    id SERIAL PRIMARY KEY,
                    region TEXT NOT NULL,
                    risk_score INTEGER NOT NULL,
                    confidence TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    embedding vector(384),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

        conn.commit()


def save_analysis(
    region,
    risk_score,
    confidence_level,
    executive_summary
):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO risk_analyses (
                    region,
                    risk_score,
                    confidence_level,
                    executive_summary
                )
                VALUES (%s, %s, %s, %s)
            """, (
                region,
                risk_score,
                confidence_level,
                executive_summary
            ))

        conn.commit()


def save_critical_alert(
    region,
    risk_score,
    executive_summary
):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO critical_alerts (
                    region,
                    risk_score,
                    executive_summary
                )
                VALUES (%s, %s, %s)
            """, (
                region,
                risk_score,
                executive_summary
            ))

        conn.commit()


def get_history(limit=10):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    region,
                    risk_score,
                    confidence_level,
                    executive_summary,
                    timestamp
                FROM risk_analyses
                ORDER BY id DESC
                LIMIT %s
            """, (limit,))

            return cur.fetchall()


def get_critical_alerts(limit=20):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    region,
                    risk_score,
                    executive_summary,
                    timestamp
                FROM critical_alerts
                ORDER BY id DESC
                LIMIT %s
            """, (limit,))

            return cur.fetchall()


init_db()