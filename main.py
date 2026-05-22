import sys
from src.graph_logic import create_supply_chain_graph


def run_risk_intelligence(region: str):
    print(f"--- INITIALIZING AUTONOMOUS RISK INTELLIGENCE FOR: {region} ---")

    risk_graph = create_supply_chain_graph()

    inputs = {
        "query": region,
        "market_risk_report": "",
        "logistics_impact": "",
        "inventory_risk_level": "",
        "final_recommendation": "",
        "risk_report": "",
        "history": []
    }

    print(f"Analyzing {region} supply chain dependencies...")

    try:
        final_state = risk_graph.invoke(inputs)

        print("\n" + "=" * 60)
        print("AI MULTI-AGENT SUPPLY CHAIN RISK REPORT")
        print("=" * 60)
        print(final_state["risk_report"])
        print("=" * 60)

    except Exception as e:
        print(f"Error during orchestration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_risk_intelligence("South China Sea Logistics")