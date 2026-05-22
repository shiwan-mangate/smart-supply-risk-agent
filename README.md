# Autonomous Supply Chain Risk Intelligence System

![Title](https://raw.githubusercontent.com/aniket-work/supply-chain-risk-intelligence/main/images/title_diagram.png)

## Overview

This repository demonstrates a **Multi-Agent Supply Chain Risk Intelligence System** built using **LangGraph**. The system automates the traditionally manual process of monitoring global signals, assessing logistics impacts, and calculating inventory risks to provide executive-level strategic recommendations.

## System Architecture

![Architecture](https://raw.githubusercontent.com/aniket-work/supply-chain-risk-intelligence/main/images/architecture_diagram.png)

The system utilizes a directed graph orchestration pattern:
1.  **Market Analyst Agent**: Monitors geopolitical and economic volatility.
2.  **Logistics Coordinator Agent**: Translates market risks into transit delays and lead-time impacts.
3.  **Inventory Strategist Agent**: Evaluates stock-out probabilities based on current safety stocks and logistics projections.
4.  **Executive Orchestrator Agent**: Synthesizes all inputs into actionable risk reports.

## Key Features

1.  **Autonomous State Management**: Precise state control using LangGraph's `TypedDict`.
2.  **Strategic Reasoning**: Moves beyond simple RAG to multi-step, multi-agent reasoning.
3.  **Real-world Applicability**: Solves a trillion-dollar business problem (Supply Chain Resilience).

## Getting Started

### Prerequisites

*   Python 3.10+
*   `langgraph`
*   `langchain-openai` (or your preferred LLM provider)

### Installation

```bash
git clone https://github.com/aniket-work/supply-chain-risk-intelligence.git
cd supply-chain-risk-intelligence
pip install -r requirements.txt
```

### Usage

```python
python main.py
```

## Performance & Design

![Flow](https://raw.githubusercontent.com/aniket-work/supply-chain-risk-intelligence/main/images/flow_diagram.png)

The system flow ensures that each agent builds upon the verified context of the previous agent, eliminating "hallucination loops" common in unstructured agent swarms.

## License

MIT
