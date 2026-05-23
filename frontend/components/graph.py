import networkx as nx
import plotly.graph_objects as go


WORKFLOW_MAP = {
    "memory": "Memory Recall",
    "recall": "Memory Recall",
    "market": "Market Intel",
    "intelligence": "Market Intel",
    "logistics": "Logistics",
    "inventory": "Inventory",
    "strategy": "Strategy",
    "competitor": "Competitor",
    "risk": "Risk Scoring",
    "store": "Memory Store",
    "critical": "Critical Escalation",
    "alert": "Critical Escalation",
}


WORKFLOW_EDGES = [
    ("Memory Recall", "Market Intel"),
    ("Market Intel", "Logistics"),
    ("Logistics", "Inventory"),
    ("Inventory", "Strategy"),
    ("Strategy", "Competitor"),
    ("Competitor", "Risk Scoring"),
    ("Risk Scoring", "Memory Store"),
    ("Risk Scoring", "Critical Escalation")
]


def extract_executed_nodes(history):
    """
    Dynamically map backend execution history to workflow nodes.
    """
    executed = set()

    if not history:
        return executed

    for item in history:
        raw_text = ""

        if isinstance(item, str):
            raw_text = item.lower()

        elif isinstance(item, dict):
            raw_text = str(
                item.get("node")
                or item.get("step")
                or item.get("agent")
                or item
            ).lower()

        for keyword, workflow_node in WORKFLOW_MAP.items():
            if keyword in raw_text:
                executed.add(workflow_node)

    return executed


def build_agent_graph(history=None):
    """
    Build dynamic execution-aware LangGraph visualization.
    """
    executed = extract_executed_nodes(history)

    all_nodes = set()

    for edge in WORKFLOW_EDGES:
        all_nodes.add(edge[0])
        all_nodes.add(edge[1])

    graph = nx.DiGraph()
    graph.add_nodes_from(all_nodes)
    graph.add_edges_from(WORKFLOW_EDGES)

    pos = nx.spring_layout(graph, seed=42)

    # --------------------
    # Edges
    # --------------------
    edge_x = []
    edge_y = []

    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        hoverinfo="none",
        line=dict(
            width=2,
            color="#64748B"
        )
    )

    # --------------------
    # Nodes
    # --------------------
    node_x = []
    node_y = []
    node_labels = []
    node_colors = []

    for node in graph.nodes():
        x, y = pos[node]

        node_x.append(x)
        node_y.append(y)
        node_labels.append(node)

        if node in executed:
            node_colors.append("#22C55E")   # completed
        elif node == "Critical Escalation":
            node_colors.append("#EF4444")   # alert
        else:
            node_colors.append("#00D9FF")   # pending

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        hoverinfo="text",
        text=node_labels,
        textposition="top center",
        marker=dict(
            size=30,
            color=node_colors,
            line=dict(
                width=2,
                color="white"
            )
        )
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="Live Agent Execution Workflow",
            template="plotly_dark",
            showlegend=False,
            hovermode="closest",
            margin=dict(l=20, r=20, t=60, b=20),
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                visible=False
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                visible=False
            ),
            height=700
        )
    )

    return fig