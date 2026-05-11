"""
Top Navigation Component — Udrive Design
Modern top navigation bar instead of sidebar.
"""

import streamlit as st
from utils.auth import current_user, logout
from config.settings import ROLES


NAV_ITEMS = [
    {"group": "Dashboards", "items": [
        ("Executive Dashboard", ["super_admin","qa_admin","qa_evaluator","team_leader","ops_manager","viewer"]),
        ("QA Insights", ["super_admin","qa_admin","qa_evaluator","team_leader","ops_manager","viewer"]),
        ("Coaching Insights", ["super_admin","qa_admin","team_leader","coach","ops_manager","viewer"]),
        ("Agent Performance", ["super_admin","qa_admin","team_leader","ops_manager","agent","viewer"]),
        ("Root Cause Analysis", ["super_admin","qa_admin","ops_manager"]),
    ]},
    {"group": "Evaluations", "items": [
        ("New Evaluation", ["super_admin","qa_admin","qa_evaluator"]),
        ("Evaluations List", ["super_admin","qa_admin","qa_evaluator","team_leader","ops_manager"]),
    ]},
    {"group": "Coaching", "items": [
        ("New Coaching Session", ["super_admin","qa_admin","team_leader","coach"]),
        ("Coaching Sessions", ["super_admin","qa_admin","team_leader","coach","ops_manager"]),
    ]},
    {"group": "Reports", "items": [
        ("Reports & Export", ["super_admin","qa_admin","qa_evaluator","team_leader","ops_manager","viewer"]),
    ]},
    {"group": "Administration", "items": [
        ("User Management", ["super_admin","qa_admin"]),
        ("Form Builder", ["super_admin","qa_admin"]),
        ("System Settings", ["super_admin"]),
        ("Audit Logs", ["super_admin","qa_admin"]),
    ]},
]


def render_topnav():
    user = current_user()
    role = user.get("role", "viewer")
    role_cfg = ROLES.get(role, {})
    current = st.session_state.get("current_page", "Executive Dashboard")

    # Build nav options for this role
    nav_options = []
    for group in NAV_ITEMS:
        for label, roles in group["items"]:
            if role in roles or role == "super_admin":
                nav_options.append(label)

    # Render top navigation bar using HTML
    st.markdown("""
        <div class="udrive-topnav">
            <div class="topnav-left">
                <div class="udrive-logo">
                    <span style="font-family:'Outfit',sans-serif;font-size:1.5rem;font-weight:800;color:#52BAEF;">Udrive</span>
                    <span style="font-family:'Outfit',sans-serif;font-size:1.5rem;font-weight:800;color:#F8FAFC;">Pro</span>
                </div>
            </div>
            <div class="topnav-center">
    """, unsafe_allow_html=True)

    # Navigation as segmented control (inline pills)
    try:
        # Try Streamlit's segmented_control (newer versions)
        selected = st.segmented_control(
            "Navigation",
            options=nav_options,
            default=current,
            key="nav_segments",
            selection_mode="single"
        )
        if selected and selected != current:
            st.session_state.current_page = selected
            st.rerun()
    except Exception:
        # Fallback to selectbox
        selected = st.selectbox(
            "Navigation",
            options=nav_options,
            index=nav_options.index(current) if current in nav_options else 0,
            key="nav_dropdown",
            label_visibility="collapsed"
        )
        if selected != current:
            st.session_state.current_page = selected

    st.markdown("""
            </div>
            <div class="topnav-right">
                <div class="user-menu">
    """, unsafe_allow_html=True)

    # User profile section
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("""
                <div style="width:40px;height:40px;border-radius:50%;background:#52BAEF;display:flex;align-items:center;justify-content:center;font-family:'Outfit',sans-serif;font-size:1rem;font-weight:700;color:#fff;">
                    U
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div style="font-family:'Outfit',sans-serif;font-size:0.875rem;font-weight:600;color:#F8FAFC;">
                    {user.get('name', 'User')}
                </div>
                <div style="font-family:'Plus+Jakarta+Sans',sans-serif;font-size:0.7rem;color:#52BAEF;text-transform:uppercase;">
                    {role_cfg.get('label', role)}
                </div>
            """, unsafe_allow_html=True)
        with col1:
            if st.button("🚪", key="logout_btn", help="Sign Out"):
                logout()

    st.markdown("""
                </div>
            </div>
        </div>
        
        <style>
        .udrive-topnav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 70px;
            background: #1E293B;
            border-bottom: 1px solid #334155;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 1.5rem;
            z-index: 9999;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        }
        .udrive-logo {
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }
        .topnav-left {
            display: flex;
            align-items: center;
            min-width: 200px;
        }
        .topnav-center {
            flex: 1;
            display: flex;
            justify-content: center;
        }
        .nav-tabs {
            display: flex;
            gap: 0.25rem;
            background: #F7F9FC;
            padding: 0.25rem;
            border-radius: 10px;
        }
        .topnav-right {
            display: flex;
            align-items: center;
            min-width: 200px;
            justify-content: flex-end;
        }
        .user-menu {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Add top padding for the fixed header
    st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)

    return st.session_state.get("current_page", "Executive Dashboard")


def render_page_selector() -> str:
    """Simple page selector that returns the current page."""
    return render_topnav()
