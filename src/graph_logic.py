import operator
from typing import Annotated, List, TypedDict

from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq

from src.config import GROQ_API_KEY, MODEL_NAME, TEMPERATURE
from src.prompts import (
    MARKET_ANALYST_PROMPT,
    LOGISTICS_PROMPT,
    INVENTORY_PROMPT,
    EXECUTIVE_PROMPT,
    RISK_REPORT_PROMPT
)
from src.schemas import RiskReportSchema
from src.logger import logger


# -------------------------
# LLM INITIALIZATION
# -------------------------
llm = ChatGroq(
    model=MODEL_NAME,
    groq_api_key=GROQ_API_KEY,
    temperature=TEMPERATURE
)

structured_llm = llm.with_structured_output(RiskReportSchema)


# -------------------------
# STATE
# -------------------------
class AgentState(TypedDict):
    query: str
    market_risk_report: str
    logistics_impact: str
    inventory_risk_level: str
    final_recommendation: str
    risk_report: str
    history: Annotated[List[str], operator.add]


# -------------------------
# AGENT 1
# -------------------------
def market_analyst_node(state: AgentState):
    logger.info("Market Analyst started")

    prompt = MARKET_ANALYST_PROMPT.format(
        query=state["query"]
    )

    response = llm.invoke(prompt)

    logger.info("Market Analyst completed")

    return {
        "market_risk_report": response.content,
        "history": ["Market analysis completed"]
    }


# -------------------------
# AGENT 2
# -------------------------
def logistics_coordinator_node(state: AgentState):
    logger.info("Logistics Coordinator started")

    prompt = LOGISTICS_PROMPT.format(
        market_signals=state["market_risk_report"]
    )

    response = llm.invoke(prompt)

    logger.info("Logistics Coordinator completed")

    return {
        "logistics_impact": response.content,
        "history": ["Logistics assessment completed"]
    }


# -------------------------
# AGENT 3
# -------------------------
def inventory_strategist_node(state: AgentState):
    logger.info("Inventory Strategist started")

    prompt = INVENTORY_PROMPT.format(
        logistics_impact=state["logistics_impact"]
    )

    response = llm.invoke(prompt)

    logger.info("Inventory Strategist completed")

    return {
        "inventory_risk_level": response.content,
        "history": ["Inventory risk assessment completed"]
    }


# -------------------------
# AGENT 4
# -------------------------
def executive_orchestrator_node(state: AgentState):
    logger.info("Executive Orchestrator started")

    prompt = EXECUTIVE_PROMPT.format(
        market=state["market_risk_report"],
        logistics=state["logistics_impact"],
        inventory=state["inventory_risk_level"]
    )

    response = llm.invoke(prompt)

    logger.info("Executive Orchestrator completed")

    return {
        "final_recommendation": response.content,
        "history": ["Executive recommendation generated"]
    }


# -------------------------
# AGENT 5
# -------------------------
def risk_reporter_node(state: AgentState):
    logger.info("Risk Reporter started")

    structured_response = structured_llm.invoke(
        RISK_REPORT_PROMPT.format(
            recommendation=state["final_recommendation"]
        )
    )

    report = f"""
Executive Summary:
{structured_response.executive_summary}

Risk Score (1-10):
{structured_response.risk_score}

Key Risks:
{chr(10).join(f"- {risk}" for risk in structured_response.key_risks)}

Recommended Actions:
{chr(10).join(f"- {action}" for action in structured_response.recommended_actions)}

Confidence Level:
{structured_response.confidence_level}
"""

    logger.info("Risk Reporter completed")

    return {
        "risk_report": report,
        "history": ["Structured risk report generated"]
    }


# -------------------------
# GRAPH
# -------------------------
def create_supply_chain_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("MarketAnalyst", market_analyst_node)
    workflow.add_node("LogisticsCoordinator", logistics_coordinator_node)
    workflow.add_node("InventoryStrategist", inventory_strategist_node)
    workflow.add_node("ExecutiveOrchestrator", executive_orchestrator_node)
    workflow.add_node("RiskReporterAgent", risk_reporter_node)

    workflow.set_entry_point("MarketAnalyst")

    workflow.add_edge("MarketAnalyst", "LogisticsCoordinator")
    workflow.add_edge("LogisticsCoordinator", "InventoryStrategist")
    workflow.add_edge("InventoryStrategist", "ExecutiveOrchestrator")
    workflow.add_edge("ExecutiveOrchestrator", "RiskReporterAgent")
    workflow.add_edge("RiskReporterAgent", END)

    return workflow.compile()