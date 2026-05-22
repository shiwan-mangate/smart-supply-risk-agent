import operator
from typing import Annotated, List, TypedDict, Dict
from langgraph.graph import StateGraph, END

# Define the state of our Supply Chain Risk Intelligence Graph
class AgentState(TypedDict):
    query: str
    market_risk_report: str
    logistics_impact: str
    inventory_risk_level: str
    final_recommendation: str
    history: Annotated[List[str], operator.add]

# --- Agent 1: Global Market Analyst ---
def market_analyst_node(state: AgentState):
    """Analyzes global market signals for geopolitical or economic risks."""
    # Simulation: In real world, this would call Tavily or News APIs
    query = state['query']
    report = f"MARKET ANALYST: Found significant volatility in {query} region. Geopolitical tensions are increasing insurance premiums for maritime transit."
    return {
        "market_risk_report": report,
        "history": ["Market Analysis Completed"]
    }

# --- Agent 2: Logistics Coordinator ---
def logistics_coordinator_node(state: AgentState):
    """Assesses transit delays and route disruptions based on market signals."""
    market_signals = state['market_risk_report']
    # Simulation: Analyze impact on routes
    impact = f"LOGISTICS COORDINATOR: Based on market signals ({market_signals}), rerouting is expected via Cape of Good Hope. Lead times projected to increase by 14 days."
    return {
        "logistics_impact": impact,
        "history": ["Logistics Assessment Completed"]
    }

# --- Agent 3: Inventory Strategist ---
def inventory_strategist_node(state: AgentState):
    """Calculates stockout risks based on transit impact and current levels."""
    logistics_impact = state['logistics_impact']
    # Simulation: Check safety stocks
    risk = f"INVENTORY STRATEGIST: Current safety stock lasts 10 days. The {logistics_impact} will cause a stockout gap of 4 days for critical SKU:CH-900."
    return {
        "inventory_risk_level": risk,
        "history": ["Inventory Risk Assessment Completed"]
    }

# --- Agent 4: Executive Orchestrator ---
def executive_orchestrator_node(state: AgentState):
    """Summarizes all risk signals and provides a strategic recommendation."""
    m_report = state['market_risk_report']
    l_impact = state['logistics_impact']
    i_risk = state['inventory_risk_level']
    
    recommendation = f"""
### STRATEGIC SUPPLY CHAIN RISK REPORT
1. MARKET: {m_report}
2. LOGISTICS: {l_impact}
3. INVENTORY: {i_risk}

**EXECUTIVE SUMMARY**: Immediate risk of stockout for critical SKUs.
**RECOMMENDED ACTION**: Accelerate air freight for 500 units of CH-900 and activate backup supplier in Mexico.
"""
    return {
        "final_recommendation": recommendation,
        "history": ["Final Recommendation Generated"]
    }

def create_supply_chain_graph():
    # Initialize the Graph
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("MarketAnalyst", market_analyst_node)
    workflow.add_node("LogisticsCoordinator", logistics_coordinator_node)
    workflow.add_node("InventoryStrategist", inventory_strategist_node)
    workflow.add_node("ExecutiveOrchestrator", executive_orchestrator_node)

    # Build Edges (Linear for this PoC, but easily made cyclic)
    workflow.set_entry_point("MarketAnalyst")
    workflow.add_edge("MarketAnalyst", "LogisticsCoordinator")
    workflow.add_edge("LogisticsCoordinator", "InventoryStrategist")
    workflow.add_edge("InventoryStrategist", "ExecutiveOrchestrator")
    workflow.add_edge("ExecutiveOrchestrator", END)

    return workflow.compile()

if __name__ == "__main__":
    # Test Run
    graph = create_supply_chain_graph()
    initial_state = {
        "query": "Middle East Corridor",
        "market_risk_report": "",
        "logistics_impact": "",
        "inventory_risk_level": "",
        "final_recommendation": "",
        "history": []
    }
    
    result = graph.invoke(initial_state)
    print(result["final_recommendation"])
