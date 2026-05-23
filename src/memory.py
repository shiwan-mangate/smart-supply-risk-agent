from fastembed import TextEmbedding
from pgvector.psycopg import register_vector

from src.database import get_connection
from src.logger import logger


class MemoryManager:
    def __init__(self):
        self.embedder = TextEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )

        with get_connection() as conn:
            register_vector(conn)

    def get_embedding(self, text: str):
        embedding = next(
            self.embedder.embed([text])
        )

        return embedding.tolist()

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

        return any(
            keyword in summary_lower
            for keyword in keywords
        )

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
            logger.info("Memory skipped")
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
                f"Recalled {len(memories)} memories"
            )

        return memories

    def format_memories(self, memories):
        if not memories:
            return "No relevant historical memories found."

        formatted = "\n\n".join(memories)

        return f"Relevant Historical Memories:\n{formatted}"