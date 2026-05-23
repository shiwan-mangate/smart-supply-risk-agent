import streamlit as st

from components.api_client import (
    get_critical_alerts,
    APIClientError
)

from components.cards import alert_card


def fetch_alerts():
    """
    Shared alerts cache loader.
    """
    if st.session_state["alerts_cache"] is None:
        st.session_state["alerts_cache"] = get_critical_alerts()

    return st.session_state["alerts_cache"]


def render_alerts():
    st.title("🚨 Critical Alerts")
    st.subheader("High-priority supply chain disruptions")

    try:
        alerts = fetch_alerts()

    except APIClientError as e:
        st.error(f"Failed to load alerts: {e}")
        return

    if not alerts:
        st.success("No critical supply disruptions detected.")
        return

    alerts = sorted(
        alerts,
        key=lambda x: x.get("risk_score", 0),
        reverse=True
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.metric("Total Critical Alerts", len(alerts))

    with col2:
        if st.button(
            "Refresh Alerts",
            key="refresh_alerts_button"
        ):
            try:
                st.session_state["alerts_cache"] = get_critical_alerts()
                st.success("Alerts refreshed.")
                st.rerun()

            except APIClientError as e:
                st.error(f"Refresh failed: {e}")

    st.divider()

    for alert in alerts:
        alert_card(
            region=alert.get("region", "Unknown"),
            risk_score=alert.get("risk_score", 0),
            summary=alert.get(
                "executive_summary",
                alert.get("summary", "No summary available.")
            ),
            timestamp=alert.get("timestamp", "")
        )

    # Latest live analysis preview
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