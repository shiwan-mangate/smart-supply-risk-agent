import operator
import asyncio
from typing import Annotated, List, TypedDict

import requests
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from src.memory import MemoryManager
from src.config import GROQ_API_KEY, NEWS_API_KEY, MODEL_NAME, TEMPERATURE
from src.prompts import (
    MARKET_ANALYST_PROMPT,
    LOGISTICS_PROMPT,
    INVENTORY_PROMPT,
    EXECUTIVE_PROMPT,
    RISK_REPORT_PROMPT,
    COMPETITOR_INTEL_PROMPT
)
from src.logger import logger


llm = ChatGroq(
    model=MODEL_NAME,
    groq_api_key=GROQ_API_KEY,
    temperature=TEMPERATURE,
    max_tokens=1500
)

memory_manager = MemoryManager()

# Global throttling
LLM_SEMAPHORE = asyncio.Semaphore(1)


class AgentState(TypedDict):
    query: str
    news_context: str
    market_risk_report: str
    logistics_impact: str
    inventory_risk_level: str
    final_recommendation: str
    competitor_status: str
    risk_report: str
    risk_score: float
    confidence_level: str
    reanalysis_count: int
    is_reanalysis: bool
    recalled_memories: str
    history: Annotated[List[str], operator.add]


def fetch_news(query: str) -> str:
    logger.info("Fetching real news data")

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "pageSize": 5,
        "sortBy": "publishedAt"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        articles = data.get("articles", [])

        if not articles:
            return "No recent news found."

        headlines = [
            f"- {article['title']}"
            for article in articles
            if article.get("title")
        ]

        return "\n".join(headlines)

    except Exception as e:
        logger.error(f"News fetch failed: {e}")
        return "News data unavailable."


async def memory_recall_node(state: AgentState):
    logger.info("Memory Recall Agent started")

    memories = memory_manager.recall(state["query"])
    recalled_context = memory_manager.format_memories(memories)

    logger.info("Memory Recall Agent completed")

    return {
        "recalled_memories": recalled_context,
        "history": ["Historical memory recalled"]
    }


async def market_analyst_node(state: AgentState):
    logger.info("Market Analyst started")

    news_context = fetch_news(state["query"])

    extra_context = ""

    if state["is_reanalysis"]:
        extra_context = """
IMPORTANT:
Previous analysis had LOW confidence.
Perform a deeper second-pass analysis.
Be more conservative and explore uncertainty.
"""

    prompt = MARKET_ANALYST_PROMPT.format(
        query=state["query"],
        recalled_memories=state["recalled_memories"][:1200],
        news_context=news_context
    ) + extra_context

    async with LLM_SEMAPHORE:
        response = await llm.ainvoke(prompt)

    logger.info("Market Analyst completed")

    return {
        "news_context": news_context,
        "market_risk_report": response.content,
        "history": ["Market analysis completed"]
    }


async def logistics_coordinator_node(state: AgentState):
    logger.info("Logistics Coordinator started")

    prompt = LOGISTICS_PROMPT.format(
        market_signals=state["market_risk_report"][:1500]
    )

    async with LLM_SEMAPHORE:
        response = await llm.ainvoke(prompt)

    logger.info("Logistics Coordinator completed")

    return {
        "logistics_impact": response.content,
        "history": ["Logistics assessment completed"]
    }


async def inventory_strategist_node(state: AgentState):
    logger.info("Inventory Strategist started")

    prompt = INVENTORY_PROMPT.format(
        logistics_impact=state["logistics_impact"][:1500]
    )

    async with LLM_SEMAPHORE:
        response = await llm.ainvoke(prompt)

    logger.info("Inventory Strategist completed")

    return {
        "inventory_risk_level": response.content,
        "history": ["Inventory risk assessment completed"]
    }


async def executive_orchestrator_node(state: AgentState):
    logger.info("Executive Orchestrator started")

    prompt = EXECUTIVE_PROMPT.format(
        market=state["market_risk_report"][:1000],
        logistics=state["logistics_impact"][:1000],
        inventory=state["inventory_risk_level"][:1000]
    )

    async with LLM_SEMAPHORE:
        response = await llm.ainvoke(prompt)

    logger.info("Executive Orchestrator completed")

    return {
        "final_recommendation": response.content,
        "history": ["Executive recommendation generated"]
    }


async def competitor_intelligence_node(state: AgentState):
    logger.info("Competitor Intelligence Agent started")

    prompt = COMPETITOR_INTEL_PROMPT.format(
        query=state["query"],
        recommendation=state["final_recommendation"][:1200],
        news_context=state["news_context"][:800]
    )

    async with LLM_SEMAPHORE:
        response = await llm.ainvoke(prompt)

    logger.info("Competitor Intelligence Agent completed")

    return {
        "competitor_status": response.content,
        "history": ["Competitor intelligence completed"]
    }


async def risk_reporter_node(state: AgentState):
    logger.info("Risk Reporter started")

    prompt = RISK_REPORT_PROMPT.format(
        recommendation=(
            state["final_recommendation"][:1200]
            + "\n"
            + state["competitor_status"][:1000]
        )
    )

    async with LLM_SEMAPHORE:
        response = await llm.ainvoke(prompt)

    report = response.content

    risk_score = 0.0
    confidence = "Unknown"

    lines = report.splitlines()

    for i, line in enumerate(lines):
        clean_line = line.strip().replace("*", "")

        if "Risk Score" in clean_line and i + 1 < len(lines):
            try:
                risk_score = float(
                    lines[i + 1].strip().replace("*", "")
                )
            except ValueError:
                risk_score = 0.0

        if "Confidence Level:" in clean_line and i + 1 < len(lines):
            confidence = (
                lines[i + 1]
                .strip()
                .replace("*", "")
            )

    logger.info("Risk Reporter completed")

    return {
        "risk_report": report,
        "risk_score": risk_score,
        "confidence_level": confidence,
        "history": ["Structured risk report generated"]
    }


async def reanalysis_node(state: AgentState):
    logger.warning("Low confidence detected — triggering reanalysis")

    return {
        "reanalysis_count": state["reanalysis_count"] + 1,
        "is_reanalysis": True,
        "history": ["Reanalysis triggered"]
    }


async def critical_alert_node(state: AgentState):
    logger.warning("Critical Alert Agent triggered")

    urgent_message = f"""
🚨 CRITICAL SUPPLY CHAIN ALERT 🚨

Risk Score: {state["risk_score"]}/10

Immediate executive escalation required.

URGENT ACTIONS:
- Activate backup suppliers immediately
- Approve premium freight budget
- Launch supply chain war-room response
- Notify executive leadership
- Increase safety stock
"""

    return {
        "risk_report": state["risk_report"] + "\n" + urgent_message,
        "history": ["Critical escalation triggered"]
    }


def route_confidence(state: AgentState):
    if (
        state["confidence_level"].lower() == "low"
        and state["reanalysis_count"] < 1
    ):
        return "reanalyze"

    return "continue"


def route_risk(state: AgentState):
    if state["risk_score"] >= 8:
        return "critical"

    return "safe"


async def passthrough_node(state: AgentState):
    return state


async def memory_store_node(state: AgentState):
    logger.info("Memory Store Agent started")

    report_lines = state["risk_report"].splitlines()
    executive_summary = "No summary available"

    for i, line in enumerate(report_lines):
        clean_line = line.strip().replace("*", "")

        if "Executive Summary:" in clean_line and i + 1 < len(report_lines):
            executive_summary = report_lines[i + 1].strip()
            break

    memory_manager.remember(
        region=state["query"],
        risk_score=state["risk_score"],
        confidence=state["confidence_level"],
        summary=executive_summary
    )

    logger.info("Memory Store Agent completed")

    return {
        "history": ["Memory stored"]
    }


def create_supply_chain_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("MemoryRecallAgent", memory_recall_node)
    workflow.add_node("MarketAnalyst", market_analyst_node)
    workflow.add_node("LogisticsCoordinator", logistics_coordinator_node)
    workflow.add_node("InventoryStrategist", inventory_strategist_node)
    workflow.add_node("ExecutiveOrchestrator", executive_orchestrator_node)
    workflow.add_node("CompetitorIntelligenceAgent", competitor_intelligence_node)
    workflow.add_node("RiskReporterAgent", risk_reporter_node)
    workflow.add_node("ReanalysisAgent", reanalysis_node)
    workflow.add_node("RiskDecision", passthrough_node)
    workflow.add_node("CriticalAlertAgent", critical_alert_node)
    workflow.add_node("MemoryStoreAgent", memory_store_node)

    workflow.set_entry_point("MemoryRecallAgent")

    workflow.add_edge("MemoryRecallAgent", "MarketAnalyst")
    workflow.add_edge("MarketAnalyst", "LogisticsCoordinator")
    workflow.add_edge("LogisticsCoordinator", "InventoryStrategist")
    workflow.add_edge("InventoryStrategist", "ExecutiveOrchestrator")
    workflow.add_edge("ExecutiveOrchestrator", "CompetitorIntelligenceAgent")
    workflow.add_edge("CompetitorIntelligenceAgent", "RiskReporterAgent")

    workflow.add_conditional_edges(
        "RiskReporterAgent",
        route_confidence,
        {
            "reanalyze": "ReanalysisAgent",
            "continue": "MemoryStoreAgent"
        }
    )

    workflow.add_edge("ReanalysisAgent", "MemoryRecallAgent")
    workflow.add_edge("MemoryStoreAgent", "RiskDecision")

    workflow.add_conditional_edges(
        "RiskDecision",
        route_risk,
        {
            "critical": "CriticalAlertAgent",
            "safe": END
        }
    )

    workflow.add_edge("CriticalAlertAgent", END)

    return workflow.compile()