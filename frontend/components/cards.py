import streamlit as st


def metric_card(title: str, value: str, delta: str = None):
    """
    Premium KPI metric card.
    """
    delta_html = f"<p style='color:#00D9FF;'>{delta}</p>" if delta else ""

    st.markdown(f"""
    <div class="metric-card">
        <h4 style="margin-bottom:10px;">{title}</h4>
        <h2 style="margin:0;">{value}</h2>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def alert_card(region: str, risk_score: int, summary: str, timestamp: str = ""):
    """
    Critical alert card.
    """
    st.markdown(f"""
    <div class="alert-card">
        <h3>🚨 {region}</h3>
        <p><strong>Risk Score:</strong> {risk_score}</p>
        <p>{summary}</p>
        <small>{timestamp}</small>
    </div>
    """, unsafe_allow_html=True)


def analysis_card(region: str, risk_score: int, confidence: str, summary: str):
    """
    Analysis result card.
    """
    st.markdown(f"""
    <div class="glass-card">
        <h3>{region}</h3>
        <p><strong>Risk Score:</strong> {risk_score}</p>
        <p><strong>Confidence:</strong> {confidence}</p>
        <p>{summary}</p>
    </div>
    """, unsafe_allow_html=True)


def summary_card(title: str, content: str):
    """
    Executive summary style card.
    """
    st.markdown(f"""
    <div class="glass-card">
        <h3>{title}</h3>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)


def success_card(title: str, content: str):
    """
    Success / recommendation card.
    """
    st.markdown(f"""
    <div class="success-card">
        <h3>{title}</h3>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)