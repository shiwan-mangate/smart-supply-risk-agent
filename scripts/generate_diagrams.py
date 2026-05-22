import base64
import requests
import os

def generate_diagram(name, code):
    encoded = base64.b64encode(code.encode()).decode()
    # Use a high contrast technical theme for the title
    url = f"https://mermaid.ink/img/{encoded}?theme=dark&bgColor=1a1a1a"
    print(f"Generating diagram: {name}")
    response = requests.get(url)
    if response.status_code == 200:
        os.makedirs('images', exist_ok=True)
        with open(f"images/{name}_diagram.png", 'wb') as f:
            f.write(response.content)
        print(f"Successfully saved images/{name}_diagram.png")
    else:
        print(f"Failed to generate diagram {name}: {response.status_code}")

diagrams = {
    "title": """
graph TD
    subgraph "Supply Chain Intelligence Hub"
        Decision[("Executive Decision Engine")]
    end
    
    Market[("Global Market Signals")] --> Engine
    Logistics[("Real-time Transit Data")] --> Engine
    Inventory[("Multimodal Store Metrics")] --> Engine
    
    Engine{{"Autonomous Risk Agent"}}
    
    Engine --> Strategic["Strategic Sourcing"]
    Engine --> Tactical["Inventory Leveling"]
    Engine --> Operational["Route Optimization"]
    
    classDef default fill:#1a1a1a,stroke:#4f46e5,stroke-width:2px,color:#fff;
    classDef highlight fill:#4f46e5,stroke:#fff,stroke-width:2px,color:#fff;
    class Engine highlight;
""",
    "architecture": """
graph LR
    User([Supply Chain Mgr]) --> UI[Streamlit Dashboard]
    UI --> Orchestrator["LangGraph Orchestrator"]
    
    subgraph Agents
        MarketAgent["Global Market Agent"]
        LogisticsAgent["Logistics Risk Agent"]
        InventoryAgent["Inventory Balance Agent"]
    end
    
    Orchestrator --> MarketAgent
    Orchestrator --> LogisticsAgent
    Orchestrator --> InventoryAgent
    
    MarketAgent --> Search["Tavily Search API"]
    LogisticsAgent --> Maps["Google Maps/Weather APIs"]
    InventoryAgent --> ERP["SAP/ERP Connector"]
    
    Agents --> Collector["Risk Intelligence Collector"]
    Collector --> Orchestrator
    Orchestrator --> Summary["Strategic Risk Report"]
""",
    "flow": """
sequenceDiagram
    participant Manager as Supply Chain Mgr
    participant Graph as LangGraph Orchestrator
    participant Market as Market Agent
    participant Logistics as Logistics Agent
    participant Inventory as Inventory Agent
    
    Manager->>Graph: Trigger Risk Analysis
    Graph->>Market: Assess Geopolitical Risks
    Market-->>Graph: Middle East Transit Issues Found
    Graph->>Logistics: Estimate Lead Time Impact
    Logistics-->>Graph: +12 Days for Suez Rerouting
    Graph->>Inventory: Check Stock Safety Levels
    Inventory-->>Graph: Alert: Stockout in 5 Days
    Graph->>Manager: Recommended: Pull Forward Singapore Order
"""
}

if __name__ == "__main__":
    for name, code in diagrams.items():
        generate_diagram(name, code)
