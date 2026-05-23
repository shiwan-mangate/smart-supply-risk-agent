import streamlit as st
import pandas as pd

from components.api_client import (
    get_history,
    APIClientError
)


def fetch_history():
    """
    Shared history cache loader.
    """
    if st.session_state["history_cache"] is None:
        st.session_state["history_cache"] = get_history()

    return st.session_state["history_cache"]


def render_history():
    st.title("📜 Intelligence History")
    st.subheader("Historical supply chain risk assessments")

    try:
        history = fetch_history()

    except APIClientError as e:
        st.error(f"Failed to load history: {e}")
        return

    if not history:
        st.info("No intelligence history available.")
        return

    df = pd.DataFrame(history)

    # Normalize schema differences
    if "confidence_level" not in df.columns and "confidence" in df.columns:
        df["confidence_level"] = df["confidence"]

    if "executive_summary" not in df.columns and "summary" in df.columns:
        df["executive_summary"] = df["summary"]

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.download_button(
            label="Download History CSV",
            data=df.to_csv(index=False),
            file_name="risk_history.csv",
            mime="text/csv"
        )

    with col2:
        if st.button(
            "Refresh History",
            key="refresh_history_button"
        ):
            try:
                st.session_state["history_cache"] = get_history()
                st.success("History refreshed.")
                st.rerun()

            except APIClientError as e:
                st.error(f"Refresh failed: {e}")

    # Latest analysis preview
    if st.session_state["latest_analysis"]:
        latest = st.session_state["latest_analysis"]

        st.divider()
        st.subheader("🧠 Latest Live Analysis")

        st.json({
            "region": latest.get("region"),
            "risk_score": latest.get("risk_score"),
            "confidence": latest.get("confidence"),
            "summary": latest.get("summary")
        })