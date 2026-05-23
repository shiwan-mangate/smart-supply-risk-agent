import uuid
from datetime import datetime

import chromadb
from sentence_transformers import SentenceTransformer

from src.logger import logger


class MemoryManager:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="memory_store")

        self.collection = self.client.get_or_create_collection(
            name="supply_chain_memories"
        )

        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    def should_store(
        self,
        risk_score: float,
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

        if any(keyword in summary_lower for keyword in keywords):
            return True

        return False

    def remember(
        self,
        region: str,
        risk_score: float,
        confidence: str,
        summary: str
    ):
        try:
            if not self.should_store(risk_score, confidence, summary):
                logger.info("Memory skipped (low importance)")
                return

            timestamp = datetime.now().isoformat()

            memory_text = f"""
Region: {region}
Risk Score: {risk_score}
Confidence: {confidence}
Summary: {summary}
Timestamp: {timestamp}
"""

            embedding = self.embedder.encode(memory_text).tolist()

            self.collection.add(
                ids=[str(uuid.uuid4())],
                documents=[memory_text],
                embeddings=[embedding],
                metadatas=[{
                    "region": region,
                    "risk_score": risk_score,
                    "confidence": confidence,
                    "timestamp": timestamp
                }]
            )

            logger.info("Memory stored successfully")

        except Exception as e:
            logger.error(f"Memory store failed: {e}")

    def recall(self, query: str, top_k: int = 3):
        try:
            query_embedding = self.embedder.encode(query).tolist()

            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )

            documents = results.get("documents", [[]])[0]

            if not documents:
                return []

            logger.info(f"Recalled {len(documents)} relevant memories")

            return documents

        except Exception as e:
            logger.error(f"Memory recall failed: {e}")
            return []

    def format_memories(self, memories):
        if not memories:
            return "No relevant historical memories found."

        formatted = "\n\n".join(memories)

        return f"Relevant Historical Memories:\n{formatted}"