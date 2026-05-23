import streamlit as st

from components.api_client import (
    get_health,
    APIClientError,
    BASE_URL
)


def fetch_health():
    """
    Shared health cache loader.
    """
    if st.session_state["health_cache"] is None:
        st.session_state["health_cache"] = get_health()

    return st.session_state["health_cache"]


def render_settings():
    st.title("⚙️ Settings & System Status")
    st.subheader("Platform configuration and operational diagnostics")

    # -------------------------
    # Backend Configuration
    # -------------------------
    st.markdown("### Backend Configuration")
    st.code(BASE_URL)

    # -------------------------
    # Health
    # -------------------------
    st.markdown("### System Health")

    try:
        health = fetch_health()

    except APIClientError as e:
        st.error(f"Health check failed: {e}")
        return

    col1, col2 = st.columns([1, 1])

    with col1:
        st.metric(
            "Backend Status",
            health.get("status", "Unknown")
        )

    with col2:
        if st.button(
            "Refresh Health",
            key="refresh_health_button"
        ):
            try:
                st.session_state["health_cache"] = get_health()
                st.success("Health refreshed.")
                st.rerun()

            except APIClientError as e:
                st.error(f"Refresh failed: {e}")

    st.json(health)

    st.divider()

    # -------------------------
    # Frontend Info
    # -------------------------
    st.markdown("### Frontend Information")

    frontend_info = {
        "frontend_name": "Sentinel Supply AI",
        "frontend_version": "1.0.0",
        "environment": "Development",
        "ui_framework": "Streamlit",
        "visual_theme": "Dark Enterprise Dashboard"
    }

    st.json(frontend_info)

    st.divider()

    # -------------------------
    # Operator Profile
    # -------------------------
    st.markdown("### Operator Profile")

    profile = {
        "name": "Admin Operator",
        "role": "Global Risk Analyst",
        "email": "admin@sentinel.ai",
        "access_level": "Enterprise"
    }

    st.json(profile)

    # -------------------------
    # Shared App State Debug
    # -------------------------
    st.divider()
    st.markdown("### Shared Session State")

    st.json({
        "latest_region": st.session_state["latest_region"],
        "latest_analysis_available": st.session_state["latest_analysis"] is not None,
        "history_cache_loaded": st.session_state["history_cache"] is not None,
        "alerts_cache_loaded": st.session_state["alerts_cache"] is not None,
        "health_cache_loaded": st.session_state["health_cache"] is not None
    })