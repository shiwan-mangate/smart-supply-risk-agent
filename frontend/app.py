import streamlit as st
from streamlit_option_menu import option_menu

from components.styles import load_css
from components.state import init_session_state

from pages.dashboard import render_dashboard
from pages.analyze import render_analyze
from pages.history import render_history
from pages.alerts import render_alerts
from pages.settings import render_settings
from pages.graph_monitor import render_graph_monitor


st.set_page_config(
    page_title="Sentinel Supply AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize shared app state
init_session_state()

# Load styling
load_css()


with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:10px;'>
        <h1 style='color:#00D9FF;'>🛡️ Sentinel Supply AI</h1>
        <p>Global Risk Command Center</p>
    </div>
    """, unsafe_allow_html=True)

    selected = option_menu(
        menu_title="Navigation",
        options=[
            "Dashboard",
            "Analyze Region",
            "History",
            "Critical Alerts",
            "Graph Monitor",
            "Settings"
        ],
        icons=[
            "speedometer2",
            "globe",
            "clock-history",
            "exclamation-triangle",
            "diagram-3",
            "gear"
        ],
        menu_icon="cast",
        default_index=0
    )


if selected == "Dashboard":
    render_dashboard()

elif selected == "Analyze Region":
    render_analyze()

elif selected == "History":
    render_history()

elif selected == "Critical Alerts":
    render_alerts()

elif selected == "Graph Monitor":
    render_graph_monitor()

elif selected == "Settings":
    render_settings()