"""
Global Theme & Style Injection — U-Drive Dark Enterprise Design System
Modern dark enterprise theme with deep navy backgrounds and neon accents.
Inspired by premium SaaS dashboards (Linear, Stripe, Notion).
"""

import streamlit as st


def inject_global_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        :root {
            --udrive-dark: #0D0D12;
            --udrive-surface: #13131A;
            --udrive-elevated: #1A1A24;
            --udrive-hover: #222230;
            --udrive-active: #2A2A38;
            --udrive-cyan: #00D4FF;
            --udrive-cyan-dim: #00A8C6;
            --udrive-violet: #8B5CF6;
            --udrive-success: #10B981;
            --udrive-warning: #F59E0B;
            --udrive-error: #EF4444;
            --udrive-info: #3B82F6;
            --udrive-border: #2D2D3A;
            --udrive-text: #F8FAFC;
            --udrive-text-secondary: #94A3B8;
            --udrive-text-muted: #64748B;
            --font-display: 'Plus Jakarta Sans', sans-serif;
            --font-body: 'Plus Jakarta Sans', sans-serif;
            --radius-md: 10px;
            --radius-lg: 16px;
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
            --shadow-glow: 0 0 20px rgba(0, 212, 255, 0.25);
        }

        html, body, [class*="css"] {
            font-family: var(--font-body) !important;
            background-color: var(--udrive-dark) !important;
            color: var(--udrive-text) !important;
        }

        .stApp { background: var(--udrive-dark) !important; }
        .block-container { padding: 1.5rem 2rem 3rem !important; max-width: 1600px !important; }
        
        section[data-testid="stSidebar"] { display: none !important; }
        [data-testid="stHeader"] { display: none !important; }

        h1, h2, h3, h4, h5, h6 {
            font-family: var(--font-display) !important;
            color: var(--udrive-text) !important;
            font-weight: 700 !important;
        }

        a { color: var(--udrive-cyan) !important; }

        input, textarea, select,
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div {
            background: var(--udrive-surface) !important;
            border: 1px solid var(--udrive-border) !important;
            color: var(--udrive-text) !important;
            border-radius: var(--radius-md) !important;
        }
        
        input:focus, textarea:focus {
            border-color: var(--udrive-cyan) !important;
            box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.15) !important;
        }

        .stButton > button {
            font-family: var(--font-display) !important;
            font-weight: 600 !important;
            border-radius: var(--radius-md) !important;
            padding: 0.625rem 1.25rem !important;
        }
        
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, var(--udrive-cyan), var(--udrive-cyan-dim)) !important;
            color: #000 !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            box-shadow: var(--shadow-glow) !important;
        }
        
        .stButton > button {
            background: var(--udrive-elevated) !important;
            color: var(--udrive-text) !important;
            border: 1px solid var(--udrive-border) !important;
        }

        [data-testid="metric-container"] {
            background: var(--udrive-surface) !important;
            border: 1px solid var(--udrive-border) !important;
            border-radius: var(--radius-lg) !important;
            padding: 1.25rem 1.5rem !important;
        }
        
        [data-testid="stMetricLabel"] { color: var(--udrive-text-muted) !important; font-size: 0.75rem !important; text-transform: uppercase; }
        [data-testid="stMetricValue"] { font-family: var(--font-display) !important; }

        .stTabs [data-baseweb="tab-list"] {
            background: var(--udrive-surface) !important;
            border-radius: var(--radius-lg) !important;
            border: 1px solid var(--udrive-border) !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: var(--udrive-text-secondary) !important;
            border-radius: var(--radius-md) !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, var(--udrive-cyan), var(--udrive-cyan-dim)) !important;
            color: #000 !important;
        }

        .dataframe, [data-testid="stDataFrame"] {
            border-radius: var(--radius-lg) !important;
            border: 1px solid var(--udrive-border) !important;
        }
        
        .dataframe th {
            background: var(--udrive-elevated) !important;
            color: var(--udrive-cyan) !important;
            font-size: 0.75rem !important;
        }
        
        .dataframe td {
            background: var(--udrive-surface) !important;
            color: var(--udrive-text) !important;
        }

        .streamlit-expanderHeader {
            background: var(--udrive-surface) !important;
            border: 1px solid var(--udrive-border) !important;
            border-radius: var(--radius-md) !important;
        }

        .stAlert {
            border-radius: var(--radius-md) !important;
            border-left: 4px solid !important;
        }
        
        .stSuccess { background: rgba(16, 185, 129, 0.1) !important; border-color: var(--udrive-success) !important; }
        .stError { background: rgba(239, 68, 68, 0.1) !important; border-color: var(--udrive-error) !important; }
        .stWarning { background: rgba(245, 158, 11, 0.1) !important; border-color: var(--udrive-warning) !important; }

        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: var(--udrive-dark); }
        ::-webkit-scrollbar-thumb { background: var(--udrive-border); border-radius: 3px; }

        .kpi-card {
            background: var(--udrive-surface);
            border: 1px solid var(--udrive-border);
            border-radius: var(--radius-lg);
            padding: 1.25rem 1.5rem;
            position: relative;
            box-shadow: var(--shadow-md);
            transition: all 0.25s ease;
        }
        
        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--udrive-cyan), var(--udrive-violet));
        }
        
        .kpi-card:hover {
            transform: translateY(-2px);
            border-color: var(--udrive-cyan);
            box-shadow: var(--shadow-glow);
        }
        
        .kpi-card-icon {
            width: 40px; height: 40px;
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            margin-bottom: 0.75rem;
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.15), rgba(139, 92, 246, 0.15));
        }
        
        .kpi-card-value {
            font-family: var(--font-display);
            font-size: 1.75rem;
            font-weight: 800;
            color: var(--udrive-text);
            line-height: 1;
        }
        
        .kpi-card-label {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--udrive-text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .kpi-card-delta {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.125rem 0.5rem;
            border-radius: 9999px;
            margin-top: 0.5rem;
        }
        
        .kpi-card-delta.positive { background: rgba(16, 185, 129, 0.15); color: var(--udrive-success); }
        .kpi-card-delta.negative { background: rgba(239, 68, 68, 0.15); color: var(--udrive-error); }

        .badge {
            display: inline-flex;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        .badge-success { background: rgba(16, 185, 129, 0.15); color: var(--udrive-success); }
        .badge-warning { background: rgba(245, 158, 11, 0.15); color: var(--udrive-warning); }
        .badge-error { background: rgba(239, 68, 68, 0.15); color: var(--udrive-error); }
        .badge-info { background: rgba(59, 130, 246, 0.15); color: var(--udrive-info); }
        .badge-violet { background: rgba(139, 92, 246, 0.15); color: var(--udrive-violet); }
        .badge-cyan { background: rgba(0, 212, 255, 0.15); color: var(--udrive-cyan); }

        .page-header { margin-bottom: 1.5rem; }
        .page-title { font-size: 1.75rem; font-weight: 800; color: var(--udrive-text); }
        .page-subtitle { font-size: 0.9375rem; color: var(--udrive-text-secondary); }

        .udrive-topnav {
            position: fixed; top: 0; left: 0; right: 0; height: 64px;
            background: var(--udrive-surface);
            border-bottom: 1px solid var(--udrive-border);
            display: flex; align-items: center; padding: 0 1.5rem;
            z-index: 9999;
            box-shadow: var(--shadow-md);
        }
        
        .udrive-logo {
            display: flex; align-items: center; gap: 0.75rem;
            font-weight: 800; font-size: 1.125rem; color: var(--udrive-text);
        }
        
        .udrive-logo-icon {
            width: 36px; height: 36px;
            background: linear-gradient(135deg, var(--udrive-cyan), var(--udrive-violet));
            border-radius: var(--radius-md);
            display: flex; align-items: center; justify-content: center;
            color: #000; font-weight: 800;
        }
        
        .udrive-nav-item {
            padding: 0.5rem 1rem;
            border-radius: var(--radius-md);
            font-size: 0.875rem; font-weight: 600;
            color: var(--udrive-text-secondary);
            cursor: pointer;
        }
        
        .udrive-nav-item:hover { background: var(--udrive-hover); color: var(--udrive-text); }
        .udrive-nav-item.active { background: rgba(0, 212, 255, 0.15); color: var(--udrive-cyan); }
        
        .udrive-user { margin-left: auto; display: flex; align-items: center; gap: 0.75rem; }
        .udrive-user-avatar {
            width: 36px; height: 36px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--udrive-cyan), var(--udrive-violet));
            display: flex; align-items: center; justify-content: center;
            color: #000; font-weight: 700;
        }
        
        .udrive-user-name { font-weight: 600; color: var(--udrive-text); font-size: 0.875rem; }
        .udrive-user-role { font-size: 0.75rem; color: var(--udrive-text-muted); }
        
        .udrive-content { padding-top: 80px; padding-left: 2rem; padding-right: 2rem; padding-bottom: 2rem; }

        .chart-container {
            background: var(--udrive-surface);
            border: 1px solid var(--udrive-border);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            box-shadow: var(--shadow-md);
        }
        
        .chart-header {
            font-size: 1rem; font-weight: 700; color: var(--udrive-text);
            margin-bottom: 1rem;
        }

        .sparkline {
            height: 32px;
            display: flex; align-items: flex-end; gap: 2px;
        }
        
        .sparkline-bar {
            flex: 1;
            background: linear-gradient(to top, var(--udrive-cyan), var(--udrive-violet));
            border-radius: 2px 2px 0 0;
            opacity: 0.6;
        }
        
        .sparkline-bar:last-child { opacity: 1; }

        .empty-state { text-align: center; padding: 3rem; color: var(--udrive-text-muted); }
        .empty-state-icon { font-size: 3rem; margin-bottom: 1rem; opacity: 0.5; }
        .empty-state-title { font-size: 1.125rem; font-weight: 700; color: var(--udrive-text-secondary); }

        .login-page {
            min-height: 100vh;
            display: flex; align-items: center; justify-content: center;
            background: var(--udrive-dark);
            padding: 2rem;
        }
        
        .login-card {
            max-width: 400px; width: 100%;
            background: var(--udrive-surface);
            border: 1px solid var(--udrive-border);
            border-radius: 24px;
            padding: 2.5rem;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
        }
        
        .login-title { font-size: 1.5rem; font-weight: 800; color: var(--udrive-text); text-align: center; margin-bottom: 0.25rem; }
        .login-subtitle { font-size: 0.875rem; color: var(--udrive-text-muted); text-align: center; margin-bottom: 2rem; }

        .dark-card {
            background: var(--udrive-surface);
            border: 1px solid var(--udrive-border);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            box-shadow: var(--shadow-md);
        }
        
        .dark-card:hover {
            border-color: var(--udrive-cyan);
            box-shadow: var(--shadow-glow);
        }
        
        .dark-card-header {
            font-size: 0.75rem; font-weight: 700;
            letter-spacing: 0.08em; text-transform: uppercase;
            color: var(--udrive-cyan); margin-bottom: 0.75rem;
        }

        @media (max-width: 768px) {
            .block-container { padding: 1rem !important; }
            .udrive-content { padding: 1rem; padding-top: 80px; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, delta: str = "", color: str = "#00D4FF", icon: str = "", sparkline_data: list = None):
    delta_html = ""
    if delta:
        is_positive = delta.startswith("+") or delta.replace("%", "").replace(".", "").isdigit()
        delta_class = "positive" if is_positive else "negative"
        arrow = "↑" if is_positive else "↓"
        delta_html = f'<div class="kpi-card-delta {delta_class}">{arrow} {delta}</div>'
    
    sparkline_html = ""
    if sparkline_data:
        bars = "".join([f'<div class="sparkline-bar" style="height:{max(4, min(28, v))}px"></div>' for v in sparkline_data])
        sparkline_html = f'<div class="sparkline">{bars}</div>'
    
    st.markdown(
        f"""
        <div class="kpi-card" style="border-top: 3px solid {color}">
            <div class="kpi-card-icon">{icon}</div>
            <div class="kpi-card-value">{value}</div>
            <div class="kpi-card-label">{label}</div>
            {delta_html}
            {sparkline_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str = ""):
    st.markdown(
        f'''<div class="page-header">
            <div class="page-title">{title}</div>
            {"<div class='page-subtitle'>" + subtitle + "</div>" if subtitle else ""}
        </div>''',
        unsafe_allow_html=True,
    )


def badge(text: str, kind: str = "info"):
    return f'<span class="badge badge-{kind}">{text}</span>'


def chart_container(title: str = None):
    header = f'<div class="chart-header">{title}</div>' if title else ""
    st.markdown(f'<div class="chart-container">{header}', unsafe_allow_html=True)


def chart_container_end():
    st.markdown('</div>', unsafe_allow_html=True)


CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Plus Jakarta Sans", color="#94A3B8", size=12),
    margin=dict(l=10, r=10, t=30, b=10),
)


def style_plotly_fig(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", color="#94A3B8", size=12),
        margin=dict(l=40, r=20, t=40, b=40),
        title=dict(font=dict(family="Plus Jakarta Sans", size=14, weight=700, color="#F8FAFC")),
        xaxis=dict(gridcolor="#2D2D3A", linecolor="#2D2D3A"),
        yaxis=dict(gridcolor="#2D2D3A", linecolor="#2D2D3A"),
    )
    fig.update_traces(marker=dict(line=dict(width=0)))
    return fig