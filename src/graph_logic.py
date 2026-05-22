import os
import operator
from typing import Annotated, List, TypedDict

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)


# -----------------------------
# STATE DEFINITION
# -----------------------------
class AgentState(TypedDict):
    query: str
    market_risk_report: str
    logistics_impact: str
    inventory_risk_level: str
    final_recommendation: str
    risk_report: str
    history: Annotated[List[str], operator.add]


# -----------------------------
# AGENT 1: MARKET ANALYST
# -----------------------------
def market_analyst_node(state: AgentState):
    """Analyzes geopolitical and market risks."""

    query = state["query"]

    prompt = f"""
    You are a Global Supply Chain Market Risk Analyst.

    Analyze the supply chain risks for this region/corridor:
    {query}

    Focus on:
    - geopolitical tensions
    - sanctions
    - fuel price volatility
    - port congestion
    - economic instability

    Return a concise professional risk assessment.
    """

    response = llm.invoke(prompt)

    return {
        "market_risk_report": response.content,
        "history": ["Market analysis completed"]
    }


# -----------------------------
# AGENT 2: LOGISTICS COORDINATOR
# -----------------------------
def logistics_coordinator_node(state: AgentState):
    """Analyzes logistics impact from market risks."""

    market_signals = state["market_risk_report"]

    prompt = f"""
    You are a Supply Chain Logistics Coordinator.

    Based on this market risk assessment:

    {market_signals}

    Analyze:
    - route disruption
    - alternate shipping routes
    - transit delay estimates
    - freight cost pressure
    - logistics bottlenecks

    Return a professional logistics impact report.
    """

    response = llm.invoke(prompt)

    return {
        "logistics_impact": response.content,
        "history": ["Logistics assessment completed"]
    }


# -----------------------------
# AGENT 3: INVENTORY STRATEGIST
# -----------------------------
def inventory_strategist_node(state: AgentState):
    """Evaluates inventory risks."""

    logistics_impact = state["logistics_impact"]

    prompt = f"""
    You are an Inventory Risk Strategist.

    Based on this logistics impact:

    {logistics_impact}

    Assess:
    - stockout risk
    - safety stock adequacy
    - critical SKU exposure
    - replenishment risk
    - operational impact

    Return a concise inventory risk assessment.
    """

    response = llm.invoke(prompt)

    return {
        "inventory_risk_level": response.content,
        "history": ["Inventory risk assessment completed"]
    }


# -----------------------------
# AGENT 4: EXECUTIVE ORCHESTRATOR
# -----------------------------
def executive_orchestrator_node(state: AgentState):
    """Synthesizes all analysis into recommendations."""

    market = state["market_risk_report"]
    logistics = state["logistics_impact"]
    inventory = state["inventory_risk_level"]

    prompt = f"""
    You are a Chief Supply Chain Strategy Officer.

    Inputs:

    MARKET RISK:
    {market}

    LOGISTICS IMPACT:
    {logistics}

    INVENTORY RISK:
    {inventory}

    Generate:
    - executive summary
    - strategic recommendation
    - mitigation actions
    - operational priorities
    """

    response = llm.invoke(prompt)

    return {
        "final_recommendation": response.content,
        "history": ["Executive recommendation generated"]
    }


# -----------------------------
# AGENT 5: RISK REPORTER
# -----------------------------
def risk_reporter_node(state: AgentState):
    """Creates structured executive risk report."""

    recommendation = state["final_recommendation"]

    prompt = f"""
    You are an Executive Risk Reporting Agent.

    Based on this supply chain recommendation:

    {recommendation}

    Generate a structured report in EXACT format:

    Executive Summary:
    <summary>

    Risk Score (1-10):
    <score>

    Key Risks:
    - risk 1
    - risk 2
    - risk 3

    Recommended Actions:
    - action 1
    - action 2
    - action 3

    Confidence Level:
    <Low / Medium / High>
    """

    response = llm.invoke(prompt)

    return {
        "risk_report": response.content,
        "history": ["Risk report generated"]
    }


# -----------------------------
# GRAPH CREATION
# -----------------------------
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


# -----------------------------
# LOCAL TEST
# -----------------------------
if __name__ == "__main__":
    graph = create_supply_chain_graph()

    initial_state = {
        "query": "South China Sea Logistics",
        "market_risk_report": "",
        "logistics_impact": "",
        "inventory_risk_level": "",
        "final_recommendation": "",
        "risk_report": "",
        "history": []
    }

    result = graph.invoke(initial_state)

    print("\n" + "=" * 60)
    print(result["risk_report"])
    print("=" * 60)