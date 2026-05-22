from langgraph.graph import StateGraph, END
from .state import AgentState
from .agents import StrategicAgents

def create_swarm() -> StateGraph:
    agents = StrategicAgents()
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("monitor", agents.monitor_agent)
    workflow.add_node("analyst", agents.analyst_agent)
    workflow.add_node("strategist", agents.strategist_agent)

    # Set entry point
    workflow.set_entry_point("monitor")

    # Add conditional edges
    workflow.add_conditional_edges(
        "monitor",
        lambda x: x["next_step"],
        {
            "analyst": "analyst",
            "end": END
        }
    )

    workflow.add_conditional_edges(
        "analyst",
        lambda x: x["next_step"],
        {
            "strategist": "strategist",
            "end": END
        }
    )

    workflow.add_conditional_edges(
        "strategist",
        lambda x: x["next_step"],
        {
            "monitor": "monitor",
            "end": END
        }
    )

    return workflow.compile()
