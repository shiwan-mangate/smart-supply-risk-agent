import pandas as pd
import plotly.express as px
import streamlit as st


def risk_trend_chart(history):
    """
    Line chart for risk score trend over time.
    """
    if not history:
        st.info("No intelligence history available for risk trend.")
        return

    df = pd.DataFrame(history)

    required_cols = {"timestamp", "risk_score"}
    if not required_cols.issubset(df.columns):
        st.warning("History data missing required fields for trend chart.")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    fig = px.line(
        df.sort_values("timestamp"),
        x="timestamp",
        y="risk_score",
        title="Risk Trend Over Time",
        markers=True
    )

    fig.update_layout(
        template="plotly_dark",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)


def confidence_distribution_chart(history):
    """
    Pie chart for confidence levels.
    """
    if not history:
        st.info("No history available for confidence distribution.")
        return

    df = pd.DataFrame(history)

    confidence_col = None

    if "confidence" in df.columns:
        confidence_col = "confidence"
    elif "confidence_level" in df.columns:
        confidence_col = "confidence_level"

    if confidence_col is None:
        st.warning("Confidence field not found.")
        return

    fig = px.pie(
        df,
        names=confidence_col,
        title="Confidence Distribution"
    )

    fig.update_layout(
        template="plotly_dark",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)


def critical_alert_chart(alerts):
    """
    Bar chart for critical alerts.
    """
    if not alerts:
        st.info("No critical alerts detected.")
        return

    df = pd.DataFrame(alerts)

    required_cols = {"region", "risk_score"}
    if not required_cols.issubset(df.columns):
        st.warning("Alert data missing required fields.")
        return

    fig = px.bar(
        df,
        x="region",
        y="risk_score",
        title="Critical Alert Risk Scores"
    )

    fig.update_layout(
        template="plotly_dark",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)


def region_comparison_chart(history):
    """
    Horizontal comparison chart by region.
    """
    if not history:
        st.info("No historical data available for comparison.")
        return

    df = pd.DataFrame(history)

    required_cols = {"region", "risk_score"}
    if not required_cols.issubset(df.columns):
        st.warning("History missing required fields.")
        return

    grouped = (
        df.groupby("region")["risk_score"]
        .mean()
        .reset_index()
        .sort_values("risk_score", ascending=True)
    )

    fig = px.bar(
        grouped,
        x="risk_score",
        y="region",
        orientation="h",
        title="Average Risk by Region"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)