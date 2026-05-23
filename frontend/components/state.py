import streamlit as st


def init_session_state():
    """
    Initialize shared frontend session state.
    """
    defaults = {
        "latest_analysis": None,
        "latest_region": None,
        "history_cache": None,
        "alerts_cache": None,
        "health_cache": None,
        "dashboard_refresh": False
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value