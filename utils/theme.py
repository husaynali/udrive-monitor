"""
Global Theme & Style Injection — Udrive Design System
Modern enterprise dashboard with Udrive branding.
"""

import streamlit as st


def inject_global_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800');
        :root {
            --udrive-primary: #52BAEF;
            --udrive-primary-dark: #3DA8D8;
            --udrive-primary-light: #7AC5F2;
            --bg-base: #F7F9FC;
            --bg-surface: #FFFFFF;
            --bg-elevated: #F0F4F8;
            --border-light: #E3EBF1;
            --border-medium: #D1DCE5;
            --accent-success: #10B981;
            --accent-warning: #F59E0B;
            --accent-danger: #EF4444;
            --text-primary: #0F172A;
            --text-secondary: #475569;
            --text-muted: #94A3B8;
            --font-display: 'Outfit', sans-serif;
            --font-body: 'Plus Jakarta Sans', sans-serif;
            --radius-sm: 6px;
            --radius-md: 10px;
            --radius-lg: 16px;
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
            --shadow-md: 0 4px 12px rgba(0,0,0,0.06);
        }
        html, body, [class*="css"] { font-family: var(--font-body) !important; background-color: var(--bg-base) !important; color: var(--text-primary) !important; }
        .stApp { background: var(--bg-base) !important; }
        .block-container { padding: 1.5rem 2rem 3rem !important; max-width: 1600px !important; }
        section[data-testid="stSidebar"] { display: none !important; }
        header[data-testid="stHeader"] { display: none !important; }
        h1, h2, h3, h4, h5 { font-family: var(--font-display) !important; color: var(--text-primary) !important; font-weight: 600 !important; }
        .stButton > button { background: linear-gradient(135deg, var(--udrive-primary), var(--udrive-primary-dark)) !important; color: #FFFFFF !important; font-family: var(--font-display) !important; font-weight: 600 !important; border: none !important; border-radius: var(--radius-md) !important; box-shadow: 0 2px 8px rgba(82,186,239,0.25) !important; }
        .stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(82,186,239,0.35) !important; }
        .stButton > button[kind="secondary"] { background: var(--bg-surface) !important; color: var(--text-primary) !important; border: 1px solid var(--border-medium) !important; box-shadow: none !important; }
        [data-testid="metric-container"] { background: var(--bg-surface) !important; border: 1px solid var(--border-light) !important; border-radius: var(--radius-lg) !important; padding: 1.25rem 1.5rem !important; box-shadow: var(--shadow-sm) !important; }
        [data-testid="stMetricLabel"] { color: var(--text-secondary) !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600 !important; }
        [data-testid="stMetricValue"] { font-family: var(--font-display) !important; color: var(--text-primary) !important; font-weight: 700 !important; font-size: 1.75rem !important; }
        .stTabs [data-baseweb="tab-list"] { background: var(--bg-surface) !important; border-radius: var(--radius-lg) !important; padding: 0.35rem !important; gap: 0.35rem; border: 1px solid var(--border-light) !important; }
        .stTabs [data-baseweb="tab"] { color: var(--text-secondary) !important; font-family: var(--font-display) !important; font-size: 0.8rem !important; font-weight: 600 !important; border-radius: var(--radius-md) !important; }
        .stTabs [aria-selected="true"] { background: var(--udrive-primary) !important; color: #FFFFFF !important; }
        .streamlit-expanderHeader { background: var(--bg-surface) !important; border: 1px solid var(--border-light) !important; border-radius: var(--radius-md) !important; color: var(--text-primary) !important; font-family: var(--font-display) !important; font-weight: 600 !important; }
        .stAlert { border-radius: var(--radius-md) !important; border: none !important; }
        .stSuccess { background: rgba(16,185,129,0.1) !important; border-left: 4px solid var(--accent-success) !important; }
        .stError { background: rgba(239,68,68,0.1) !important; border-left: 4px solid var(--accent-danger) !important; }
        .stWarning { background: rgba(245,158,11,0.1) !important; border-left: 4px solid var(--accent-warning) !important; }
        .stInfo { background: rgba(82,186,239,0.1) !important; border-left: 4px solid var(--udrive-primary) !important; }
        hr { border-color: var(--border-light) !important; margin: 1.5rem 0 !important; }
        .dataframe, [data-testid="stDataFrame"] { border-radius: var(--radius-lg) !important; overflow: hidden !important; border: 1px solid var(--border-light) !important; }
        .dataframe th { background: var(--bg-elevated) !important; color: var(--text-primary) !important; font-family: var(--font-display) !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 700 !important; }
        .dataframe td { background: var(--bg-surface) !important; color: var(--text-primary) !important; border-color: var(--border-light) !important; }
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg-elevated); border-radius: 4px; }
        ::-webkit-scrollbar-thumb { background: var(--border-medium); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
        .udrive-card { background: var(--bg-surface); border: 1px solid var(--border-light); border-radius: var(--radius-lg); padding: 1.5rem; margin-bottom: 1rem; box-shadow: var(--shadow-sm); transition: all 0.3s ease; }
        .udrive-card:hover { border-color: var(--udrive-primary); box-shadow: var(--shadow-md); }
        .udrive-card-header { font-family: var(--font-display); font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--udrive-primary); margin-bottom: 0.75rem; }
        .badge { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 999px; font-family: var(--font-display); font-size: 0.7rem; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; }
        .badge-pass { background: rgba(16,185,129,0.1); color: var(--accent-success); border: 1px solid rgba(16,185,129,0.3); }
        .badge-fail { background: rgba(239,68,68,0.1); color: var(--accent-danger); border: 1px solid rgba(239,68,68,0.3); }
        .badge-nogi { background: rgba(239,68,68,0.15); color: var(--accent-danger); border: 1px solid var(--accent-danger); }
        .badge-warning { background: rgba(245,158,11,0.1); color: var(--accent-warning); border: 1px solid rgba(245,158,11,0.3); }
        .badge-info { background: rgba(82,186,239,0.1); color: var(--udrive-primary); border: 1px solid rgba(82,186,239,0.25); }
        .page-title { font-family: var(--font-display); font-size: 1.75rem; font-weight: 700; letter-spacing: -0.03em; color: var(--text-primary); margin-bottom: 0.25rem; line-height: 1.2; }
        .page-subtitle { font-family: var(--font-body); font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 1.5rem; }
        .score-display { font-family: var(--font-display); font-size: 2.5rem; font-weight: 700; line-height: 1; }
        .stProgress > div > div > div { background: linear-gradient(90deg, var(--udrive-primary), var(--udrive-primary-light)) !important; border-radius: 999px !important; }
        .stFormSubmitButton > button { background: linear-gradient(135deg, var(--udrive-primary), var(--udrive-primary-dark)) !important; color: #FFFFFF !important; font-family: var(--font-display) !important; font-weight: 600 !important; border: none !important; border-radius: var(--radius-md) !important; box-shadow: 0 4px 15px rgba(82,186,239,0.3) !important; }
        </style>
        """
    )


def kpi_card(label: str, value: str, delta: str = "", color: str = "#52BAEF", icon: str = ""):
    """Render a styled KPI card."""
    delta_html = ""
    if delta:
        arrow = "↑" if delta.startswith("+") else "↓"
        clr = "#10B981" if delta.startswith("+") else "#EF4444"
        delta_html = f'<div style="font-size:0.78rem;color:{clr};margin-top:0.25rem;font-family:var(--font-body)">{arrow} {delta}</div>'

    st.markdown(
        f"""
        <div class="udrive-card" style="border-top:3px solid {color}">
            <div class="udrive-card-header">{icon} {label}</div>
            <div class="score-display" style="color:{color};font-size:2rem">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str = ""):
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def badge(text: str, kind: str = "info"):
    return f'<span class="badge badge-{kind}">{text}</span>'
