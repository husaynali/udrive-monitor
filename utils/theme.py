"""
Global Theme & Style Injection — U-Drive Design System
Dark industrial theme with vivid accent colors.
"""

import streamlit as st


def inject_global_styles():
    st.markdown(
        """
        <style>
        /* ── Google Fonts ─────────────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=JetBrains+Mono:wght@400;600&display=swap');

        /* ── CSS Variables ────────────────────────────────── */
        :root {
            --bg-base:       #0D0F14;
            --bg-surface:    #161920;
            --bg-elevated:   #1E2130;
            --bg-border:     #2A2E45;
            --accent-primary:#00D4FF;
            --accent-second: #FF4B6E;
            --accent-green:  #00E5A0;
            --accent-amber:  #FFB800;
            --accent-purple: #9D7BFF;
            --text-primary:  #F0F2FF;
            --text-secondary:#8B92B5;
            --text-muted:    #4A5075;
            --font-display:  'Syne', sans-serif;
            --font-body:     'DM Sans', sans-serif;
            --font-mono:     'JetBrains Mono', monospace;
            --radius-sm:     6px;
            --radius-md:     12px;
            --radius-lg:     20px;
            --shadow-card:   0 4px 24px rgba(0,0,0,0.4);
            --shadow-glow:   0 0 20px rgba(0,212,255,0.15);
        }

        /* ── Base Reset ───────────────────────────────────── */
        html, body, [class*="css"] {
            font-family: var(--font-body) !important;
            background-color: var(--bg-base) !important;
            color: var(--text-primary) !important;
        }

        /* ── Sidebar ──────────────────────────────────────── */
        section[data-testid="stSidebar"] {
            background: var(--bg-surface) !important;
            border-right: 1px solid var(--bg-border) !important;
        }
        section[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

        /* ── Streamlit Overrides ──────────────────────────── */
        .stApp { background: var(--bg-base) !important; }
        .block-container { padding: 1.5rem 2rem 3rem !important; max-width: 1600px !important; }

        /* ── Headings ─────────────────────────────────────── */
        h1, h2, h3, h4, h5 {
            font-family: var(--font-display) !important;
            color: var(--text-primary) !important;
            letter-spacing: -0.02em;
        }

        /* ── Inputs ───────────────────────────────────────── */
        input, textarea, select,
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div {
            background: var(--bg-elevated) !important;
            border: 1px solid var(--bg-border) !important;
            color: var(--text-primary) !important;
            border-radius: var(--radius-sm) !important;
            font-family: var(--font-body) !important;
        }
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: var(--accent-primary) !important;
            box-shadow: 0 0 0 2px rgba(0,212,255,0.15) !important;
        }

        /* ── Buttons ──────────────────────────────────────── */
        .stButton > button {
            background: linear-gradient(135deg, var(--accent-primary), #0099CC) !important;
            color: #000 !important;
            font-family: var(--font-display) !important;
            font-weight: 700 !important;
            font-size: 0.85rem !important;
            letter-spacing: 0.05em !important;
            border: none !important;
            border-radius: var(--radius-sm) !important;
            padding: 0.5rem 1.25rem !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(0,212,255,0.35) !important;
        }
        .stButton > button[kind="secondary"] {
            background: var(--bg-elevated) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--bg-border) !important;
        }

        /* ── Metrics ──────────────────────────────────────── */
        [data-testid="metric-container"] {
            background: var(--bg-surface) !important;
            border: 1px solid var(--bg-border) !important;
            border-radius: var(--radius-md) !important;
            padding: 1rem 1.25rem !important;
        }
        [data-testid="stMetricLabel"] { color: var(--text-secondary) !important; font-size: 0.78rem !important; text-transform: uppercase; letter-spacing: 0.08em; }
        [data-testid="stMetricValue"] { font-family: var(--font-display) !important; color: var(--text-primary) !important; }
        [data-testid="stMetricDelta"] { font-size: 0.82rem !important; }

        /* ── DataFrames / Tables ──────────────────────────── */
        .dataframe, [data-testid="stDataFrame"] {
            border-radius: var(--radius-md) !important;
            overflow: hidden !important;
        }
        .dataframe th {
            background: var(--bg-elevated) !important;
            color: var(--accent-primary) !important;
            font-family: var(--font-display) !important;
            font-size: 0.78rem !important;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }
        .dataframe td {
            background: var(--bg-surface) !important;
            color: var(--text-primary) !important;
            border-color: var(--bg-border) !important;
        }

        /* ── Tabs ─────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {
            background: var(--bg-surface) !important;
            border-radius: var(--radius-md) !important;
            padding: 0.25rem !important;
            gap: 0.25rem;
            border: 1px solid var(--bg-border) !important;
        }
        .stTabs [data-baseweb="tab"] {
            color: var(--text-secondary) !important;
            font-family: var(--font-display) !important;
            font-size: 0.83rem !important;
            font-weight: 600 !important;
            border-radius: var(--radius-sm) !important;
            padding: 0.4rem 1rem !important;
        }
        .stTabs [aria-selected="true"] {
            background: var(--accent-primary) !important;
            color: #000 !important;
        }

        /* ── Expander ─────────────────────────────────────── */
        .streamlit-expanderHeader {
            background: var(--bg-surface) !important;
            border: 1px solid var(--bg-border) !important;
            border-radius: var(--radius-sm) !important;
            color: var(--text-primary) !important;
            font-family: var(--font-display) !important;
        }
        .streamlit-expanderContent {
            background: var(--bg-elevated) !important;
            border: 1px solid var(--bg-border) !important;
        }

        /* ── Alerts ───────────────────────────────────────── */
        .stAlert { border-radius: var(--radius-md) !important; }
        .stSuccess { background: rgba(0,229,160,0.1) !important; border-color: var(--accent-green) !important; }
        .stError   { background: rgba(255,75,110,0.1) !important; border-color: var(--accent-second) !important; }
        .stWarning { background: rgba(255,184,0,0.1)  !important; border-color: var(--accent-amber) !important; }
        .stInfo    { background: rgba(0,212,255,0.08) !important; border-color: var(--accent-primary) !important; }

        /* ── Divider ──────────────────────────────────────── */
        hr { border-color: var(--bg-border) !important; }

        /* ── Scrollbar ────────────────────────────────────── */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: var(--bg-base); }
        ::-webkit-scrollbar-thumb { background: var(--bg-border); border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

        /* ── Custom Card ──────────────────────────────────── */
        .qa-card {
            background: var(--bg-surface);
            border: 1px solid var(--bg-border);
            border-radius: var(--radius-md);
            padding: 1.25rem 1.5rem;
            margin-bottom: 1rem;
            box-shadow: var(--shadow-card);
            transition: border-color 0.2s ease;
        }
        .qa-card:hover { border-color: rgba(0,212,255,0.3); }
        .qa-card-header {
            font-family: var(--font-display);
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--accent-primary);
            margin-bottom: 0.75rem;
        }

        /* ── Status Badges ────────────────────────────────── */
        .badge {
            display: inline-block;
            padding: 0.2rem 0.65rem;
            border-radius: 999px;
            font-family: var(--font-display);
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }
        .badge-pass    { background: rgba(0,229,160,0.15); color: #00E5A0; border: 1px solid rgba(0,229,160,0.3); }
        .badge-fail    { background: rgba(255,75,110,0.15); color: #FF4B6E; border: 1px solid rgba(255,75,110,0.3); }
        .badge-nogo    { background: rgba(255,75,110,0.25); color: #FF4B6E; border: 1px solid #FF4B6E; }
        .badge-warning { background: rgba(255,184,0,0.15);  color: #FFB800; border: 1px solid rgba(255,184,0,0.3); }
        .badge-info    { background: rgba(0,212,255,0.12);  color: #00D4FF; border: 1px solid rgba(0,212,255,0.25); }
        .badge-purple  { background: rgba(157,123,255,0.15);color: #9D7BFF; border: 1px solid rgba(157,123,255,0.3); }

        /* ── Page Title ───────────────────────────────────── */
        .page-title {
            font-family: var(--font-display);
            font-size: 1.9rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            color: var(--text-primary);
            margin-bottom: 0.25rem;
            line-height: 1.1;
        }
        .page-subtitle {
            font-family: var(--font-body);
            font-size: 0.9rem;
            color: var(--text-secondary);
            margin-bottom: 1.5rem;
        }

        /* ── Score Ring visual ────────────────────────────── */
        .score-display {
            font-family: var(--font-display);
            font-size: 3rem;
            font-weight: 800;
            line-height: 1;
        }

        /* ── Sidebar nav item ─────────────────────────────── */
        .nav-item {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            padding: 0.5rem 0.75rem;
            border-radius: var(--radius-sm);
            cursor: pointer;
            font-family: var(--font-body);
            font-size: 0.88rem;
            color: var(--text-secondary);
            transition: all 0.15s ease;
            margin-bottom: 0.15rem;
        }
        .nav-item:hover { background: var(--bg-elevated); color: var(--text-primary); }
        .nav-item.active { background: rgba(0,212,255,0.1); color: var(--accent-primary); border-left: 3px solid var(--accent-primary); }
        </style>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, delta: str = "", color: str = "#00D4FF", icon: str = ""):
    """Render a styled KPI card."""
    delta_html = ""
    if delta:
        arrow = "↑" if delta.startswith("+") else "↓"
        clr = "#00E5A0" if delta.startswith("+") else "#FF4B6E"
        delta_html = f'<div style="font-size:0.78rem;color:{clr};margin-top:0.25rem;font-family:var(--font-body)">{arrow} {delta}</div>'

    st.markdown(
        f"""
        <div class="qa-card" style="border-top:3px solid {color}">
            <div class="qa-card-header">{icon} {label}</div>
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
