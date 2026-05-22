import sys
from src.graph_logic import create_supply_chain_graph

def run_risk_intelligence(region: str):
    print(f"--- INITIALIZING AUTONOMOUS RISK INTELLIGENCE FOR: {region} ---")
    
    # Initialize the Multi-Agent System
    risk_graph = create_supply_chain_graph()
    
    # Define Initial Input State
    inputs = {
        "query": region,
        "market_risk_report": "",
        "logistics_impact": "",
        "inventory_risk_level": "",
        "final_recommendation": "",
        "history": []
    }
    
    # Execute the Graph
    print(f"Analyzing {region} supply chain dependencies...")
    try:
        final_state = risk_graph.invoke(inputs)
        
        print("\n" + "="*50)
        print("GEN AI MULTI-AGENT ANALYSIS OUTPUT")
        print("="*50)
        print(final_state["final_recommendation"])
        print("="*50)
        
    except Exception as e:
        print(f"An error occurred during multi-agent orchestration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    region_to_analyze = "South China Sea Logistics"
    run_risk_intelligence(region_to_analyze)
