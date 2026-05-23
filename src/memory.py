import requests
from pgvector.psycopg import register_vector

from src.config import HF_API_TOKEN
from src.database import get_connection
from src.logger import logger


HF_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class MemoryManager:
    def __init__(self):
        self.api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{HF_EMBEDDING_MODEL}"
        self.headers = {
            "Authorization": f"Bearer {HF_API_TOKEN}"
        }

        with get_connection() as conn:
            register_vector(conn)

    def get_embedding(self, text: str):
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json={
                "inputs": text
            },
            timeout=60
        )

        response.raise_for_status()

        embedding = response.json()

        if isinstance(embedding[0], list):
            return embedding[0]

        return embedding

    def should_store(
        self,
        risk_score: int,
        confidence: str,
        summary: str
    ) -> bool:
        if risk_score >= 7:
            return True

        if confidence.lower() == "high":
            return True

        keywords = [
            "sanction",
            "war",
            "disruption",
            "port closure",
            "fuel crisis",
            "critical"
        ]

        summary_lower = summary.lower()

        return any(keyword in summary_lower for keyword in keywords)

    def remember(
        self,
        region: str,
        risk_score: int,
        confidence: str,
        summary: str
    ):
        if not self.should_store(
            risk_score,
            confidence,
            summary
        ):
            logger.info("Memory skipped (low importance)")
            return

        embedding = self.get_embedding(summary)

        with get_connection() as conn:
            register_vector(conn)

            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO agent_memories (
                        region,
                        risk_score,
                        confidence,
                        summary,
                        embedding
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    region,
                    risk_score,
                    confidence,
                    summary,
                    embedding
                ))

            conn.commit()

        logger.info("Memory stored successfully")

    def recall(
        self,
        query: str,
        top_k: int = 3
    ):
        query_embedding = self.get_embedding(query)

        with get_connection() as conn:
            register_vector(conn)

            with conn.cursor() as cur:
                cur.execute("""
                    SELECT summary
                    FROM agent_memories
                    ORDER BY embedding <-> %s
                    LIMIT %s
                """, (
                    query_embedding,
                    top_k
                ))

                rows = cur.fetchall()

        memories = [row[0] for row in rows]

        if memories:
            logger.info(
                f"Recalled {len(memories)} relevant memories"
            )

        return memories

    def format_memories(self, memories):
        if not memories:
            return "No relevant historical memories found."

        formatted = "\n\n".join(memories)

        return f"Relevant Historical Memories:\n{formatted}"