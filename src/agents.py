from .state import AgentState
from .tools import search_market_trends, analyze_competitor_data

class StrategicAgents:
    def monitor_agent(self, state: AgentState) -> AgentState:
        """Agent that monitors market trends."""
        print("--- MONITOR AGENT ---")
        query = state.get("focus", "Generative AI")
        finding = search_market_trends(query)
        state["findings"].append(finding)
        state["next_step"] = "analyst"
        return state

    def analyst_agent(self, state: AgentState) -> AgentState:
        """Agent that analyzes findings and competitor data."""
        print("--- ANALYST AGENT ---")
        findings = state["findings"]
        analysis = f"Analysis of findings: {', '.join(findings)}. This suggests a strong market shift."
        state["insights"].append(analysis)
        state["next_step"] = "strategist"
        return state

    def strategist_agent(self, state: AgentState) -> AgentState:
        """Agent that develops strategic recommendations."""
        print("--- STRATEGIST AGENT ---")
        insights = state["insights"]
        strategy = f"Strategic Recommendation: Focus on differentiation through specialized services. Based on: {', '.join(insights)}"
        state["report"] = strategy
        state["next_step"] = "end"
        return state
