"""
QA Evaluation, Coaching & Performance Management Platform
Main Application Entry Point — Production (SQLite-backed)
Udrive Branding Applied
"""

import streamlit as st
from config.settings import APP_CONFIG
from utils.database import init_db
from utils.auth import init_session, require_auth
from utils.theme import inject_global_styles
from components.topnav import render_topnav

# Page config
st.set_page_config(
    page_title="Udrive Pro — Performance Management Platform",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_global_styles()

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
