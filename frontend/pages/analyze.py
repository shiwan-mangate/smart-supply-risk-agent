import time
import streamlit as st

from components.api_client import (
    analyze_region,
    get_history,
    get_critical_alerts,
    APIClientError
)

from components.cards import (
    metric_card,
    summary_card,
    success_card
)

from components.graph import build_agent_graph


def render_analysis_result(result):
    """
    Shared renderer for analysis output.
    """
    st.success("Analysis complete.")

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card(
            "Region",
            result.get("region", "Unknown")
        )

    with col2:
        metric_card(
            "Risk Score",
            str(result.get("risk_score", "N/A"))
        )

    with col3:
        metric_card(
            "Confidence",
            result.get("confidence", "N/A")
        )

    st.divider()

    state = result.get("state", {})
    history = state.get("history", [])

    tabs = st.tabs([
        "Executive Summary",
        "Agent Outputs",
        "Memory",
        "Execution Trace",
        "Full Report"
    ])

    # -------------------------
    # Executive Summary
    # -------------------------
    with tabs[0]:
        summary_card(
            "Executive Summary",
            result.get("summary", "No summary available.")
        )

        success_card(
            "Final Recommendation",
            state.get(
                "final_recommendation",
                "No recommendation available."
            )
        )

    # -------------------------
    # Agent Outputs
    # -------------------------
    with tabs[1]:
        with st.expander("Market Intelligence", expanded=True):
            st.write(
                state.get(
                    "market_risk_report",
                    "No market intelligence available."
                )
            )

        with st.expander("Logistics Impact"):
            st.write(
                state.get(
                    "logistics_impact",
                    "No logistics impact available."
                )
            )

        with st.expander("Inventory Risk"):
            st.write(
                state.get(
                    "inventory_risk_level",
                    "No inventory analysis available."
                )
            )

        with st.expander("Competitor Intelligence"):
            st.write(
                state.get(
                    "competitor_status",
                    "No competitor intelligence available."
                )
            )

    # -------------------------
    # Memory
    # -------------------------
    with tabs[2]:
        recalled = state.get(
            "recalled_memories",
            "No memory recall available."
        )

        summary_card(
            "Historical Memory Recall",
            str(recalled)
        )

    # -------------------------
    # Execution Trace
    # -------------------------
    with tabs[3]:
        fig = build_agent_graph(history)
        st.plotly_chart(fig, use_container_width=True)

        if history:
            st.write("Execution History:")
            st.json(history)
        else:
            st.info("No execution history available from backend.")

    # -------------------------
    # Full Report
    # -------------------------
    with tabs[4]:
        st.json(result)


def render_analyze():
    st.title("🌍 Analyze Supply Chain Risk")
    st.subheader("Run autonomous AI geopolitical risk intelligence")

    region = st.text_input(
        "Enter region / disruption zone",
        placeholder="Example: Red Sea Conflict",
        key="analyze_region_input"
    )

    if st.button(
        "Analyze Risk",
        use_container_width=True,
        key="analyze_button"
    ):
        if not region.strip():
            st.warning("Please enter a region.")
            return

        try:
            with st.spinner("Running autonomous intelligence analysis..."):
                progress = st.progress(0)
                status_placeholder = st.empty()

                stages = [
                    "Memory Recall...",
                    "Market Intelligence...",
                    "Logistics Analysis...",
                    "Inventory Assessment...",
                    "Competitor Monitoring...",
                    "Risk Scoring..."
                ]

                for i, stage in enumerate(stages):
                    status_placeholder.caption(stage)
                    progress.progress((i + 1) / len(stages))
                    time.sleep(0.3)

                result = analyze_region(region)

                # Clear temporary UI
                progress.empty()
                status_placeholder.empty()

                # Shared app state
                st.session_state["latest_analysis"] = result
                st.session_state["latest_region"] = region

                # Refresh caches safely
                try:
                    st.session_state["history_cache"] = get_history()
                except APIClientError:
                    pass

                try:
                    st.session_state["alerts_cache"] = get_critical_alerts()
                except APIClientError:
                    pass

        except APIClientError as e:
            st.error(f"Analysis failed: {e}")
            return

        render_analysis_result(result)

    elif (
        st.session_state["latest_analysis"] is not None
        and not region.strip()
    ):
        render_analysis_result(
            st.session_state["latest_analysis"]
        )