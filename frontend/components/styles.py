import streamlit as st


def load_css():
    st.markdown("""
    <style>
    
    /* Global background */
    .stApp {
        background: linear-gradient(135deg, #0B1020, #121A2A);
        color: white;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(18, 26, 42, 0.95);
        border-right: 1px solid rgba(0, 217, 255, 0.15);
    }

    /* Glass card effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
    }

    /* Metric cards */
    .metric-card {
        background: rgba(0, 217, 255, 0.08);
        border: 1px solid rgba(0, 217, 255, 0.18);
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 25px rgba(0, 217, 255, 0.15);
    }

    /* Alert cards */
    .alert-card {
        background: rgba(255, 59, 59, 0.08);
        border: 1px solid rgba(255, 59, 59, 0.25);
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 16px;
    }

    /* Success cards */
    .success-card {
        background: rgba(34, 197, 94, 0.08);
        border: 1px solid rgba(34, 197, 94, 0.25);
        border-radius: 16px;
        padding: 18px;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00D9FF, #0099CC);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0 8px 20px rgba(0, 217, 255, 0.25);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 10px 16px;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.04);
        border-radius: 10px;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #0B1020;
    }

    ::-webkit-scrollbar-thumb {
        background: #00D9FF;
        border-radius: 10px;
    }

    /* Hide Streamlit branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    </style>
    """, unsafe_allow_html=True)