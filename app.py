"""
QA Evaluation, Coaching & Performance Management Platform
Main Application Entry Point — Production (SQLite-backed)
Udrive Branding Applied
"""

import streamlit as st
from config.settings import APP_CONFIG
from utils.database import init_db
from utils.auth import init_session, require_auth
from components.topnav import render_topnav

# Page config
st.set_page_config(
    page_title="Udrive Pro — Performance Management Platform",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inject Udrive theme CSS directly - simple version
st.markdown(r'''
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600');

* { font-family: "Plus Jakarta Sans", sans-serif; }
html, body { background-color: #F7F9FC; color: #0F172A; }
.stApp { background-color: #F7F9FC; }
.block-container { padding: 1.5rem 2rem 3rem; max-width: 1600px; }
section[data-testid="stSidebar"] { display: none; }
header[data-testid="stHeader"] { display: none; }
h1, h2, h3, h4, h5 { font-family: "Outfit", sans-serif; color: #0F172A; font-weight: 600; }
.stButton > button { background-color: #52BAEF; color: #FFFFFF; font-family: "Outfit", sans-serif; font-weight: 600; border: none; border-radius: 10px; }
.stButton > button:hover { background-color: #3DA8D8; }
[data-testid="metric-container"] { background-color: #FFFFFF; border: 1px solid #E3EBF1; border-radius: 16px; padding: 1.25rem 1.5rem; }
[data-testid="stMetricLabel"] { color: #475569; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; }
[data-testid="stMetricValue"] { font-family: "Outfit", sans-serif; color: #0F172A; font-weight: 700; font-size: 1.75rem; }
.stTabs [data-baseweb="tab-list"] { background-color: #FFFFFF; border-radius: 16px; padding: 0.35rem; gap: 0.35rem; border: 1px solid #E3EBF1; }
.stTabs [data-baseweb="tab"] { color: #475569; font-family: "Outfit", sans-serif; font-size: 0.8rem; font-weight: 600; border-radius: 10px; }
.stTabs [aria-selected="true"] { background-color: #52BAEF; color: #FFFFFF; }
.streamlit-expanderHeader { background-color: #FFFFFF; border: 1px solid #E3EBF1; border-radius: 10px; color: #0F172A; font-family: "Outfit", sans-serif; font-weight: 600; }
.stSuccess { background-color: rgba(16,185,129,0.1); border-left: 4px solid #10B981; }
.stError { background-color: rgba(239,68,68,0.1); border-left: 4px solid #EF4444; }
.stWarning { background-color: rgba(245,158,11,0.1); border-left: 4px solid #F59E0B; }
.stInfo { background-color: rgba(82,186,239,0.1); border-left: 4px solid #52BAEF; }
hr { border-color: #E3EBF1; margin: 1.5rem 0; }
.dataframe, [data-testid="stDataFrame"] { border-radius: 16px; overflow: hidden; border: 1px solid #E3EBF1; }
.dataframe th { background-color: #F0F4F8; color: #0F172A; font-family: "Outfit", sans-serif; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 700; }
.dataframe td { background-color: #FFFFFF; color: #0F172A; border-color: #E3EBF1; }
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #F0F4F8; border-radius: 4px; }
::-webkit-scrollbar-thumb { background: #D1DCE5; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #94A3B8; }
.udrive-card { background-color: #FFFFFF; border: 1px solid #E3EBF1; border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem; }
.udrive-card-header { font-family: "Outfit", sans-serif; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #52BAEF; margin-bottom: 0.75rem; }
.badge { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 999px; font-family: "Outfit", sans-serif; font-size: 0.7rem; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; }
.badge-pass { background-color: rgba(16,185,129,0.1); color: #10B981; }
.badge-fail { background-color: rgba(239,68,68,0.1); color: #EF4444; }
.badge-nogi { background-color: rgba(239,68,68,0.15); color: #EF4444; }
.badge-warning { background-color: rgba(245,158,11,0.1); color: #F59E0B; }
.badge-info { background-color: rgba(82,186,239,0.1); color: #52BAEF; }
.page-title { font-family: "Outfit", sans-serif; font-size: 1.75rem; font-weight: 700; letter-spacing: -0.03em; color: #0F172A; margin-bottom: 0.25rem; line-height: 1.2; }
.page-subtitle { font-family: "Plus Jakarta Sans", sans-serif; font-size: 0.9rem; color: #475569; margin-bottom: 1.5rem; }
.score-display { font-family: "Outfit", sans-serif; font-size: 2.5rem; font-weight: 700; line-height: 1; }
.stProgress > div > div > div { background-color: #52BAEF; border-radius: 999px; }
.stFormSubmitButton > button { background-color: #52BAEF; color: #FFFFFF; font-family: "Outfit", sans-serif; font-weight: 600; border: none; border-radius: 10px; }
</style>
''', unsafe_allow_html=True)

# Initialise database ONCE per process
@st.cache_resource
def _boot_db():
    init_db()
    return True

_boot_db()
init_session()


def main():
    if not st.session_state.get("authenticated"):
        from pages.login import render_login
        render_login()
        return

    page = render_topnav()

    if page == "Executive Dashboard":
        from pages.dashboard_executive import render
    elif page == "QA Insights":
        from pages.dashboard_qa import render
    elif page == "Coaching Insights":
        from pages.dashboard_coaching import render
    elif page == "Agent Performance":
        from pages.dashboard_agent import render
    elif page == "Root Cause Analysis":
        from pages.dashboard_rca import render
    elif page == "New Evaluation":
        from pages.evaluation_form import render
    elif page == "Evaluations List":
        from pages.evaluations_list import render
    elif page == "New Coaching Session":
        from pages.coaching_form import render
    elif page == "Coaching Sessions":
        from pages.coaching_list import render
    elif page == "Reports & Export":
        from pages.reports import render
    elif page == "User Management":
        from pages.admin_users import render
    elif page == "Form Builder":
        from pages.admin_form_builder import render
    elif page == "System Settings":
        from pages.admin_settings import render
    elif page == "Audit Logs":
        from pages.audit_logs import render
    else:
        from pages.dashboard_executive import render

    render()


if __name__ == "__main__":
    main()
