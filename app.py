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

# Inject Udrive theme CSS directly - Udrive brand colors
st.markdown(r'''
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display');

/* UDRI COLOR PALETTE */
:root {
    --udrive-blue: #52BAEF;
    --udrive-dark: #1A2744;
    --udrive-light: #E8F4FD;
    --udrive-cyan: #00D4FF;
    --bg-primary: #F7F9FC;
    --bg-white: #FFFFFF;
    --text-primary: #1A2744;
    --text-secondary: #5A6783;
    --text-muted: #94A3B8;
    --border-light: #E3EBF1;
    --success: #10B981;
    --warning: #F59E0B;
    --danger: #EF4444;
}

* { font-family: "Plus Jakarta Sans", sans-serif; }
html, body { background-color: var(--bg-primary); color: var(--text-primary); }
.stApp { background-color: var(--bg-primary); }
.block-container { padding: 1.5rem 2rem 3rem; max-width: 1600px; }
section[data-testid="stSidebar"] { display: none; }
header[data-testid="stHeader"] { display: none; }
h1, h2, h3, h4, h5 { font-family: "Outfit", sans-serif; color: var(--text-primary); font-weight: 700; }

/* Buttons - Udrive Blue */
.stButton > button { 
    background-color: var(--udrive-blue) !important; 
    color: #FFFFFF !important; 
    font-family: "Outfit", sans-serif !important; 
    font-weight: 600 !important; 
    border: none !important; 
    border-radius: 10px !important;
    box-shadow: 0 4px 12px rgba(82, 190, 239, 0.25) !important;
}
.stButton > button:hover { 
    background-color: #3DA8D8 !important; 
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(82, 190, 239, 0.35) !important;
}
.stButton > button[kind="secondary"] { 
    background-color: var(--bg-white) !important; 
    color: var(--text-primary) !important; 
    border: 1px solid var(--border-light) !important;
    box-shadow: none !important;
}

/* Metrics - White cards */
[data-testid="metric-container"] { 
    background-color: var(--bg-white); 
    border: 1px solid var(--border-light); 
    border-radius: 16px; 
    padding: 1.25rem 1.5rem; 
    box-shadow: 0 2px 8px rgba(26, 39, 68, 0.04);
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

/* Tabs */
.stTabs [data-baseweb="tab-list"] { 
    background-color: var(--bg-white); 
    border-radius: 12px; 
    padding: 0.35rem; 
    gap: 0.35rem; 
    border: 1px solid var(--border-light); 
}
.stTabs [data-baseweb="tab"] { 
    color: var(--text-secondary); 
    font-family: "Outfit", sans-serif; 
    font-size: 0.8rem; 
    font-weight: 600; 
    border-radius: 10px; 
}
.stTabs [aria-selected="true"] { 
    background-color: var(--udrive-blue); 
    color: #FFFFFF; 
}

/* Expanders */
.streamlit-expanderHeader { 
    background-color: var(--bg-white); 
    border: 1px solid var(--border-light); 
    border-radius: 12px; 
    color: var(--text-primary); 
    font-family: "Outfit", sans-serif; 
    font-weight: 600; 
}

/* Alerts */
.stSuccess { background-color: rgba(16,185,129,0.1); border-left: 4px solid var(--success); }
.stError { background-color: rgba(239,68,68,0.1); border-left: 4px solid var(--danger); }
.stWarning { background-color: rgba(245,158,11,0.1); border-left: 4px solid var(--warning); }
.stInfo { background-color: rgba(82,190,239,0.1); border-left: 4px solid var(--udrive-blue); }

/* Tables */
hr { border-color: var(--border-light); margin: 1.5rem 0; }
.dataframe, [data-testid="stDataFrame"] { border-radius: 16px; overflow: hidden; border: 1px solid var(--border-light); }
.dataframe th { 
    background-color: var(--bg-primary); 
    color: var(--text-primary); 
    font-family: "Outfit", sans-serif; 
    font-size: 0.75rem; 
    text-transform: uppercase; 
    letter-spacing: 0.06em; 
    font-weight: 700; 
}
.dataframe td { 
    background-color: var(--bg-white); 
    color: var(--text-primary); 
    border-color: var(--border-light); 
}

/* Scrollbar */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: var(--bg-primary); border-radius: 4px; }
::-webkit-scrollbar-thumb { background: #D1DCE5; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* Custom Udri Components */
.udrive-card { 
    background-color: var(--bg-white); 
    border: 1px solid var(--border-light); 
    border-radius: 16px; 
    padding: 1.5rem; 
    margin-bottom: 1rem; 
    transition: all 0.3s ease;
}
.udrive-card:hover { 
    border-color: var(--udrive-blue); 
    box-shadow: 0 4px 16px rgba(26, 39, 68, 0.08);
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

/* Badges */
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
.badge-pass { background-color: rgba(16,185,129,0.1); color: var(--success); }
.badge-fail { background-color: rgba(239,68,68,0.1); color: var(--danger); }
.badge-nogi { background-color: rgba(239,68,68,0.15); color: var(--danger); }
.badge-warning { background-color: rgba(245,158,11,0.1); color: var(--warning); }
.badge-info { background-color: rgba(82,190,239,0.1); color: var(--udrive-blue); }

/* Page Headers */
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

/* Progress */
.stProgress > div > div > div { background-color: var(--udrive-blue); border-radius: 999px; }

/* Form Submit */
.stFormSubmitButton > button { 
    background-color: var(--udrive-blue); 
    color: #FFFFFF; 
    font-family: "Outfit", sans-serif; 
    font-weight: 600; 
    border: none; 
    border-radius: 10px; 
    box-shadow: 0 4px 12px rgba(82, 190, 239, 0.3);
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
