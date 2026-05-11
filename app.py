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

# Inject Udrive theme CSS directly - Udrive DARK theme
st.markdown(r'''
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display');

/* UDRI DARK COLOR PALETTE */
:root {
    --udrive-blue: #52BAEF;
    --udrive-cyan: #00D4FF;
    --bg-dark: #0F172A;
    --bg-darker: #020617;
    --bg-card: #1E293B;
    --bg-hover: #334155;
    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
    --text-muted: #64748B;
    --border: #334155;
    --success: #10B981;
    --warning: #F59E0B;
    --danger: #EF4444;
}

* { font-family: "Plus Jakarta Sans", sans-serif; }

html, body { 
    background-color: var(--bg-darker) !important; 
    color: var(--text-primary) !important; 
}

.stApp { 
    background-color: var(--bg-dark) !important; 
}

/* Override Streamlit dark mode */
div[data-theme="dark"], 
.stApp > div,
.block-container {
    background-color: var(--bg-dark) !important;
    color: var(--text-primary) !important;
}

/* Input fields dark */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border-color: var(--border) !important;
}

.block-container { 
    padding: 1.5rem 2rem 3rem; 
    max-width: 1600px; 
    background-color: var(--bg-dark) !important;
}

section[data-testid="stSidebar"] { display: none; }
header[data-testid="stHeader"] { display: none; }
h1, h2, h3, h4, h5 { 
    font-family: "Outfit", sans-serif; 
    color: var(--text-primary); 
    font-weight: 700; 
}

/* Buttons - Udri Blue on Dark */
.stButton > button { 
    background-color: var(--udrive-blue) !important; 
    color: #0F172A !important; 
    font-family: "Outfit", sans-serif !important; 
    font-weight: 600 !important; 
    border: none !important; 
    border-radius: 10px !important;
}
.stButton > button:hover { 
    background-color: var(--udrive-cyan) !important; 
}
.stButton > button[kind="secondary"] { 
    background-color: var(--bg-card) !important; 
    color: var(--text-primary) !important; 
    border: 1px solid var(--border) !important;
}

/* Metrics - Dark cards */
[data-testid="metric-container"] { 
    background-color: var(--bg-card) !important; 
    border: 1px solid var(--border) !important; 
    border-radius: 16px; 
    padding: 1.25rem 1.5rem; 
}
[data-testid="stMetricLabel"] { 
    color: var(--text-secondary); 
    font-size: 0.75rem; 
    text-transform: uppercase; 
    letter-spacing: 0.08em; 
    font-weight: 600; 
}
[data-testid="stMetricValue"] { 
    font-family: "Outfit", sans-serif; 
    color: var(--text-primary); 
    font-weight: 700; 
    font-size: 1.75rem; 
}

/* Tabs dark */
.stTabs [data-baseweb="tab-list"] { 
    background-color: var(--bg-card) !important; 
    border-radius: 12px; 
    padding: 0.35rem; 
    gap: 0.35rem; 
    border: 1px solid var(--border) !important; 
}
.stTabs [data-baseweb="tab"] { 
    color: var(--text-secondary); 
    font-family: "Outfit", sans-serif; 
    font-size: 0.8rem; 
    font-weight: 600; 
    border-radius: 10px; 
}
.stTabs [aria-selected="true"] { 
    background-color: var(--udrive-blue) !important; 
    color: #0F172A !important; 
}

/* Expanders dark */
.streamlit-expanderHeader { 
    background-color: var(--bg-card) !important; 
    border: 1px solid var(--border) !important; 
    border-radius: 12px; 
    color: var(--text-primary) !important; 
    font-family: "Outfit", sans-serif; 
    font-weight: 600; 
}

/* Alerts dark */
.stSuccess { background-color: rgba(16,185,129,0.15) !important; border-left: 4px solid var(--success) !important; color: var(--success) !important; }
.stError { background-color: rgba(239,68,68,0.15) !important; border-left: 4px solid var(--danger) !important; color: var(--danger) !important; }
.stWarning { background-color: rgba(245,158,11,0.15) !important; border-left: 4px solid var(--warning) !important; color: var(--warning) !important; }
.stInfo { background-color: rgba(82,190,239,0.15) !important; border-left: 4px solid var(--udrive-blue) !important; color: var(--udrive-blue) !important; }

/* Tables dark */
hr { border-color: var(--border); margin: 1.5rem 0; }
.dataframe, [data-testid="stDataFrame"] { 
    border-radius: 16px; 
    overflow: hidden; 
    border: 1px solid var(--border) !important; 
    background-color: var(--bg-card) !important;
}
.dataframe th { 
    background-color: var(--bg-hover) !important; 
    color: var(--text-primary); 
    font-family: "Outfit", sans-serif; 
    font-size: 0.75rem; 
    text-transform: uppercase; 
    letter-spacing: 0.06em; 
    font-weight: 700; 
}
.dataframe td { 
    background-color: var(--bg-card) !important; 
    color: var(--text-primary); 
    border-color: var(--border) !important; 
}

/* Scrollbar dark */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: var(--bg-darker); border-radius: 4px; }
::-webkit-scrollbar-thumb { background: var(--bg-hover); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* Custom Udri Components dark */
.udrive-card { 
    background-color: var(--bg-card); 
    border: 1px solid var(--border); 
    border-radius: 16px; 
    padding: 1.5rem; 
    margin-bottom: 1rem; 
}
.udrive-card:hover { 
    border-color: var(--udrive-blue); 
}
.udrive-card-header { 
    font-family: "Outfit", sans-serif; 
    font-size: 0.7rem; 
    font-weight: 700; 
    letter-spacing: 0.1em; 
    text-transform: uppercase; 
    color: var(--udrive-blue); 
    margin-bottom: 0.75rem; 
}

/* Badges dark */
.badge { 
    display: inline-block; 
    padding: 0.25rem 0.75rem; 
    border-radius: 999px; 
    font-family: "Outfit", sans-serif; 
    font-size: 0.7rem; 
    font-weight: 600; 
    letter-spacing: 0.04em; 
    text-transform: uppercase; 
}
.badge-pass { background-color: rgba(16,185,129,0.15); color: var(--success); }
.badge-fail { background-color: rgba(239,68,68,0.15); color: var(--danger); }
.badge-nogi { background-color: rgba(239,68,68,0.25); color: var(--danger); }
.badge-warning { background-color: rgba(245,158,11,0.15); color: var(--warning); }
.badge-info { background-color: rgba(82,190,239,0.15); color: var(--udrive-blue); }

/* Page Headers dark */
.page-title { 
    font-family: "Outfit", sans-serif; 
    font-size: 1.75rem; 
    font-weight: 700; 
    letter-spacing: -0.03em; 
    color: var(--text-primary); 
    margin-bottom: 0.25rem; 
    line-height: 1.2; 
}
.page-subtitle { 
    font-family: "Plus Jakarta Sans", sans-serif; 
    font-size: 0.9rem; 
    color: var(--text-secondary); 
    margin-bottom: 1.5rem; 
}
.score-display { 
    font-family: "Outfit", sans-serif; 
    font-size: 2.5rem; 
    font-weight: 700; 
    line-height: 1; 
}

/* Progress dark */
.stProgress > div > div > div { background-color: var(--udrive-blue); border-radius: 999px; }

/* Form Submit dark */
.stFormSubmitButton > button { 
    background-color: var(--udrive-blue); 
    color: #0F172A; 
    font-family: "Outfit", sans-serif; 
    font-weight: 600; 
    border: none; 
    border-radius: 10px; 
}

/* Navigation dark */
.udrive-topnav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 70px;
    background: var(--bg-card);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 1.5rem;
    z-index: 9999;
}
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
