import streamlit as st

from components.api_client import (
    analyze_region,
    get_history,
    get_critical_alerts,
    APIClientError
)

from components.graph import build_agent_graph


def render_graph_monitor():
    st.title("🧠 LangGraph Execution Monitor")
    st.subheader("Live AI workflow execution observability")

    # -------------------------
    # Reuse latest analysis if available
    # -------------------------
    if st.session_state["latest_analysis"]:
        latest = st.session_state["latest_analysis"]

        st.info(
            f"Using latest analysis for: "
            f"{latest.get('region', 'Unknown Region')}"
        )

        col1, col2 = st.columns([2, 1])

        with col1:
            use_latest = st.button(
                "Use Latest Analysis",
                key="use_latest_graph_button",
                use_container_width=True
            )

        with col2:
            run_fresh = st.button(
                "Run Fresh Analysis",
                key="fresh_graph_button",
                use_container_width=True
            )

        if use_latest:
            state = latest.get("state", {})
            history = state.get("history", [])

            fig = build_agent_graph(history)

            st.plotly_chart(fig, use_container_width=True)

            st.divider()
            st.markdown("### Execution History")

            if history:
                st.json(history)
            else:
                st.info("No execution history available.")

            st.divider()
            st.markdown("### Raw State Payload")
            st.json(state)

            return

    # -------------------------
    # Fresh execution
    # -------------------------
    region = st.text_input(
        "Enter region to visualize workflow execution",
        placeholder="Example: Red Sea Conflict",
        key="graph_region_input"
    )

    if st.button(
        "Run Execution Monitor",
        use_container_width=True,
        key="graph_monitor_button"
    ):
        if not region.strip():
            st.warning("Please enter a region.")
            return

        try:
            with st.spinner("Running live workflow analysis..."):
                result = analyze_region(region)

                # Update shared session state
                st.session_state["latest_analysis"] = result
                st.session_state["latest_region"] = region

                # Refresh caches
                st.session_state["history_cache"] = get_history()
                st.session_state["alerts_cache"] = get_critical_alerts()

        except APIClientError as e:
            st.error(f"Execution monitoring failed: {e}")

            if st.session_state["latest_analysis"]:
                st.warning(
                    "Using latest successful analysis instead."
                )

                latest = st.session_state["latest_analysis"]
                state = latest.get("state", {})
                history = state.get("history", [])

                fig = build_agent_graph(history)
                st.plotly_chart(fig, use_container_width=True)

                st.divider()
                st.markdown("### Execution History")

                if history:
                    st.json(history)

                return