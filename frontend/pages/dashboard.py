import streamlit as st

from components.api_client import (
    get_health,
    get_history,
    get_critical_alerts,
    APIClientError
)

from components.cards import (
    metric_card,
    alert_card
)

from components.charts import (
    risk_trend_chart,
    confidence_distribution_chart,
    critical_alert_chart,
    region_comparison_chart
)


def fetch_dashboard_data():
    """
    Shared dashboard/session cache loader.
    """
    if st.session_state["health_cache"] is None:
        st.session_state["health_cache"] = get_health()

    if st.session_state["history_cache"] is None:
        st.session_state["history_cache"] = get_history()

    if st.session_state["alerts_cache"] is None:
        st.session_state["alerts_cache"] = get_critical_alerts()

    return (
        st.session_state["health_cache"],
        st.session_state["history_cache"],
        st.session_state["alerts_cache"]
    )


def render_dashboard():
    st.title("🛡️ Sentinel Supply AI")
    st.subheader("AI-Powered Global Supply Risk Command Center")

    try:
        health, history, alerts = fetch_dashboard_data()

    except APIClientError as e:
        st.error(f"Dashboard failed to load: {e}")
        return

    # -------------------------
    # KPI METRICS
    # -------------------------
    total_analyses = len(history)
    critical_count = len(alerts)

    avg_risk = 0

    if history:
        valid_scores = [
            item.get("risk_score", 0)
            for item in history
            if isinstance(item, dict)
        ]

        if valid_scores:
            avg_risk = round(sum(valid_scores) / len(valid_scores), 2)

    health_status = health.get("status", "Unknown")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Total Analyses", str(total_analyses))

    with col2:
        metric_card("Critical Alerts", str(critical_count))

    with col3:
        metric_card("Average Risk", str(avg_risk))

    with col4:
        metric_card("System Health", health_status)

    st.divider()

    # -------------------------
    # CHARTS
    # -------------------------
    col1, col2 = st.columns(2)

    with col1:
        risk_trend_chart(history)

    with col2:
        confidence_distribution_chart(history)

    col3, col4 = st.columns(2)

    with col3:
        critical_alert_chart(alerts)

    with col4:
        region_comparison_chart(history)

    st.divider()

    # -------------------------
    # LATEST ANALYSIS PREVIEW
    # -------------------------
    if st.session_state["latest_analysis"]:
        latest = st.session_state["latest_analysis"]

        st.subheader("🧠 Latest Live Analysis")

        st.markdown(f"""
        <div class="glass-card">
            <h3>{latest.get("region", "Unknown")}</h3>
            <p><strong>Risk Score:</strong> {latest.get("risk_score", "N/A")}</p>
            <p><strong>Confidence:</strong> {latest.get("confidence", "N/A")}</p>
            <p>{latest.get("summary", "No summary available.")}</p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

    # -------------------------
    # RECENT ACTIVITY
    # -------------------------
    st.subheader("📈 Recent Intelligence Activity")

    if history:
        recent = history[:5]

        for item in recent:
            st.markdown(
                f"""
                <div class="glass-card">
                    <h4>{item.get('region', 'Unknown Region')}</h4>
                    <p><strong>Risk Score:</strong> {item.get('risk_score', 'N/A')}</p>
                    <p><strong>Confidence:</strong> {item.get('confidence_level', item.get('confidence', 'N/A'))}</p>
                    <p>{item.get('executive_summary', item.get('summary', 'No summary available.'))}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("No historical intelligence available.")

    st.divider()

    # -------------------------
    # ALERT FEED
    # -------------------------
    st.subheader("🚨 Critical Alert Feed")

    if alerts:
        for alert in alerts[:5]:
            alert_card(
                region=alert.get("region", "Unknown"),
                risk_score=alert.get("risk_score", 0),
                summary=alert.get(
                    "executive_summary",
                    alert.get("summary", "No summary available.")
                ),
                timestamp=alert.get("timestamp", "")
            )
    else:
        st.success("No critical supply disruptions detected.")