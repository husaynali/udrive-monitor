"""
Global Theme & Style Injection — U-Drive Enterprise Design System
Modern enterprise theme with deep navy, purple/violet gradients, and white backgrounds.
Inspired by premium SaaS dashboards (Stripe, Linear, Notion).
"""

import streamlit as st


# ── U-Drive Brand Colors ──────────────────────────────────────────────
BRAND_COLORS = {
    "primary_navy": "#1A1E3C",
    "primary_navy_light": "#252B52",
    "primary_navy_lighter": "#2D3555",
    "accent_violet": "#7C3AED",
    "accent_violet_light": "#8B5CF6",
    "accent_violet_dark": "#6D28D9",
    "accent_cyan": "#06B6D4",
    "accent_cyan_light": "#22D3EE",
    "white": "#FFFFFF",
    "light_gray": "#F8FAFC",
    "medium_gray": "#E2E8F0",
    "dark_gray": "#64748B",
    "text_primary": "#1E293B",
    "text_secondary": "#64748B",
    "text_muted": "#94A3B8",
    "success": "#10B981",
    "warning": "#F59E0B",
    "error": "#EF4444",
    "info": "#3B82F6",
}


def inject_global_styles():
    st.markdown(
        """
        <style>
        /* ── Google Fonts ─────────────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

        /* ── CSS Variables ────────────────────────────────── */
        :root {
            /* Primary Colors - Deep Navy */
            --udrive-navy: #1A1E3C;
            --udrive-navy-light: #252B52;
            --udrive-navy-lighter: #2D3555;
            
            /* Accent - Modern Violet/Purple */
            --udrive-violet: #7C3AED;
            --udrive-violet-light: #8B5CF6;
            --udrive-violet-dark: #6D28D9;
            
            /* Secondary Accent - Cyan */
            --udrive-cyan: #06B6D4;
            --udrive-cyan-light: #22D3EE;
            
            /* Neutrals */
            --udrive-white: #FFFFFF;
            --udrive-bg: #F8FAFC;
            --udrive-bg-secondary: #F1F5F9;
            --udrive-border: #E2E8F0;
            --udrive-border-light: #F1F5F9;
            
            /* Text */
            --udrive-text: #1E293B;
            --udrive-text-secondary: #64748B;
            --udrive-text-muted: #94A3B8;
            
            /* Semantic */
            --udrive-success: #10B981;
            --udrive-warning: #F59E0B;
            --udrive-error: #EF4444;
            --udrive-info: #3B82F6;
            
            /* Typography */
            --font-display: 'Plus Jakarta Sans', sans-serif;
            --font-body: 'Inter', sans-serif;
            
            /* Spacing & Radius */
            --space-xs: 4px;
            --space-sm: 8px;
            --space-md: 16px;
            --space-lg: 24px;
            --space-xl: 32px;
            --space-2xl: 48px;
            
            --radius-sm: 6px;
            --radius-md: 10px;
            --radius-lg: 16px;
            --radius-xl: 24px;
            --radius-full: 9999px;
            
            /* Shadows - Soft & Modern */
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
            --shadow-card: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
            --shadow-elevated: 0 10px 40px -10px rgba(26, 30, 60, 0.25);
        }

        /* ── Base Reset ───────────────────────────────────── */
        html, body, [class*="css"] {
            font-family: var(--font-body) !important;
            background-color: var(--udrive-bg) !important;
            color: var(--udrive-text) !important;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        /* ── Streamlit Overrides ──────────────────────────── */
        .stApp {
            background: var(--udrive-bg) !important;
        }
        
        .block-container {
            padding: 1.5rem 2rem 3rem !important;
            max-width: 1600px !important;
        }

        /* ── Sidebar – Hide traditional sidebar ──────── */
        section[data-testid="stSidebar"] {
            display: none !important;
        }

        /* ── Top Navigation Bar ───────────────────────── */
        [data-testid="stHeader"] {
            display: none !important;
        }
        
        /* ── Headings ─────────────────────────────────────── */
        h1, h2, h3, h4, h5, h6 {
            font-family: var(--font-display) !important;
            color: var(--udrive-text) !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }
        
        h1 { font-size: 2rem !important; }
        h2 { font-size: 1.5rem !important; }
        h3 { font-size: 1.25rem !important; }

        /* ── Links ───────────────────────────────────────── */
        a, .stMarkdown a {
            color: var(--udrive-violet) !important;
            text-decoration: none !important;
        }
        a:hover {
            color: var(--udrive-violet-dark) !important;
        }

        /* ── Inputs ───────────────────────────────────────── */
        input, textarea, select,
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div,
        .stDateInput > div > div > input {
            background: var(--udrive-white) !important;
            border: 1px solid var(--udrive-border) !important;
            color: var(--udrive-text) !important;
            border-radius: var(--radius-md) !important;
            font-family: var(--font-body) !important;
            padding: 0.625rem 0.875rem !important;
            transition: all 0.2s ease !important;
        }
        
        input:focus, textarea:focus, select:focus {
            border-color: var(--udrive-violet) !important;
            box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1) !important;
            outline: none !important;
        }
        
        input::placeholder {
            color: var(--udrive-text-muted) !important;
        }

        /* ── Buttons ──────────────────────────────────────── */
        .stButton > button {
            font-family: var(--font-display) !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            letter-spacing: 0.02em !important;
            border: none !important;
            border-radius: var(--radius-md) !important;
            padding: 0.625rem 1.25rem !important;
            transition: all 0.2s ease !important;
        }
        
        /* Primary Button - Violet Gradient */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, var(--udrive-violet), var(--udrive-violet-dark)) !important;
            color: var(--udrive-white) !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 8px 20px rgba(124, 58, 237, 0.35) !important;
        }
        
        /* Secondary Button */
        .stButton > button {
            background: var(--udrive-white) !important;
            color: var(--udrive-text) !important;
            border: 1px solid var(--udrive-border) !important;
        }
        
        .stButton > button:hover {
            background: var(--udrive-bg-secondary) !important;
            border-color: var(--udrive-violet) !important;
        }

        /* ── Metrics ──────────────────────────────────────── */
        [data-testid="metric-container"] {
            background: var(--udrive-white) !important;
            border: 1px solid var(--udrive-border) !important;
            border-radius: var(--radius-lg) !important;
            padding: 1.25rem 1.5rem !important;
            box-shadow: var(--shadow-card) !important;
        }
        
        [data-testid="stMetricLabel"] {
            color: var(--udrive-text-secondary) !important;
            font-size: 0.75rem !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600 !important;
        }
        
        [data-testid="stMetricValue"] {
            font-family: var(--font-display) !important;
            color: var(--udrive-text) !important;
            font-weight: 700 !important;
        }
        
        [data-testid="stMetricDelta"] {
            font-size: 0.8rem !important;
            font-weight: 600 !important;
        }

        /* ── Tabs ─────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {
            background: var(--udrive-white) !important;
            border-radius: var(--radius-lg) !important;
            padding: 4px !important;
            gap: 4px;
            border: 1px solid var(--udrive-border) !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: var(--udrive-text-secondary) !important;
            font-family: var(--font-display) !important;
            font-size: 0.875rem !important;
            font-weight: 600 !important;
            border-radius: var(--radius-md) !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.2s ease !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, var(--udrive-violet), var(--udrive-violet-dark)) !important;
            color: var(--udrive-white) !important;
            box-shadow: var(--shadow-md) !important;
        }

        /* ── DataFrames / Tables ──────────────────────────── */
        .dataframe, [data-testid="stDataFrame"] {
            border-radius: var(--radius-lg) !important;
            overflow: hidden !important;
            border: 1px solid var(--udrive-border) !important;
        }
        
        .dataframe th {
            background: var(--udrive-bg-secondary) !important;
            color: var(--udrive-text) !important;
            font-family: var(--font-display) !important;
            font-size: 0.75rem !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-bottom: 1px solid var(--udrive-border) !important;
        }
        
        .dataframe td {
            background: var(--udrive-white) !important;
            color: var(--udrive-text) !important;
            border-color: var(--udrive-border-light) !important;
        }
        
        .dataframe tr:nth-child(even) td {
            background: var(--udrive-bg) !important;
        }
        
        .dataframe tr:hover td {
            background: var(--udrive-bg-secondary) !important;
        }

        /* ── Expander ──────────────────────────────────────── */
        .streamlit-expanderHeader {
            background: var(--udrive-white) !important;
            border: 1px solid var(--udrive-border) !important;
            border-radius: var(--radius-md) !important;
            color: var(--udrive-text) !important;
            font-family: var(--font-display) !important;
            font-weight: 600 !important;
        }
        
        .streamlit-expanderContent {
            background: var(--udrive-bg) !important;
            border: 1px solid var(--udrive-border) !important;
            border-top: none !important;
        }

        /* ── Selectbox / Dropdown ─────────────────────────── */
        [data-baseweb="select"] > div {
            background: var(--udrive-white) !important;
            border-color: var(--udrive-border) !important;
            border-radius: var(--radius-md) !important;
        }

        /* ── Alerts / Messages ───────────────────────────────── */
        .stAlert {
            border-radius: var(--radius-md) !important;
            border-left: 4px solid !important;
        }
        
        .stSuccess {
            background: rgba(16, 185, 129, 0.08) !important;
            border-color: var(--udrive-success) !important;
            color: var(--udrive-success) !important;
        }
        
        .stError {
            background: rgba(239, 68, 68, 0.08) !important;
            border-color: var(--udrive-error) !important;
            color: var(--udrive-error) !important;
        }
        
        .stWarning {
            background: rgba(245, 158, 11, 0.08) !important;
            border-color: var(--udrive-warning) !important;
            color: var(--udrive-warning) !important;
        }
        
        .stInfo {
            background: rgba(59, 130, 246, 0.08) !important;
            border-color: var(--udrive-info) !important;
            color: var(--udrive-info) !important;
        }

        /* ── Divider ──────────────────────────────────────── */
        hr {
            border-color: var(--udrive-border) !important;
        }

        /* ── Scrollbar ────────────────────────────────────── */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: var(--udrive-bg);
        }
        ::-webkit-scrollbar-thumb {
            background: var(--udrive-border);
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--udrive-text-muted);
        }

        /* ── Progress Bar ─────────────────────────────────── */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, var(--udrive-violet), var(--udrive-violet-light)) !important;
        }

        /* ── Spinner ──────────────────────────────────────── */
        .stSpinner > div {
            border-color: var(--udrive-violet) !important;
            border-top-color: transparent !important;
        }

        /* ── Custom Enterprise Card ─────────────────────── */
        .enterprise-card {
            background: var(--udrive-white);
            border: 1px solid var(--udrive-border);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            box-shadow: var(--shadow-card);
            transition: all 0.2s ease;
        }
        
        .enterprise-card:hover {
            box-shadow: var(--shadow-lg);
            border-color: rgba(124, 58, 237, 0.3);
        }
        
        .enterprise-card-header {
            font-family: var(--font-display);
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--udrive-violet);
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* ── KPI Card ─────────────────────────────────────── */
        .kpi-card {
            background: var(--udrive-white);
            border: 1px solid var(--udrive-border);
            border-radius: var(--radius-lg);
            padding: 1.25rem 1.5rem;
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-card);
            transition: all 0.25s ease;
        }
        
        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--udrive-violet), var(--udrive-cyan));
        }
        
        .kpi-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-elevated);
        }
        
        .kpi-card-icon {
            width: 40px;
            height: 40px;
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            margin-bottom: 0.75rem;
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.1), rgba(6, 182, 212, 0.1));
        }
        
        .kpi-card-value {
            font-family: var(--font-display);
            font-size: 1.75rem;
            font-weight: 800;
            color: var(--udrive-text);
            line-height: 1;
            margin-bottom: 0.25rem;
        }
        
        .kpi-card-label {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--udrive-text-secondary);
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
            border-radius: var(--radius-full);
            margin-top: 0.5rem;
        }
        
        .kpi-card-delta.positive {
            background: rgba(16, 185, 129, 0.1);
            color: var(--udrive-success);
        }
        
        .kpi-card-delta.negative {
            background: rgba(239, 68, 68, 0.1);
            color: var(--udrive-error);
        }

        /* ── Status Badges ──────────────────────────────── */
        .badge {
            display: inline-flex;
            align-items: center;
            padding: 0.25rem 0.75rem;
            border-radius: var(--radius-full);
            font-family: var(--font-display);
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }
        
        .badge-success {
            background: rgba(16, 185, 129, 0.1);
            color: var(--udrive-success);
        }
        
        .badge-warning {
            background: rgba(245, 158, 11, 0.1);
            color: var(--udrive-warning);
        }
        
        .badge-error {
            background: rgba(239, 68, 68, 0.1);
            color: var(--udrive-error);
        }
        
        .badge-info {
            background: rgba(59, 130, 246, 0.1);
            color: var(--udrive-info);
        }
        
        .badge-violet {
            background: rgba(124, 58, 237, 0.1);
            color: var(--udrive-violet);
        }

        /* ── Page Header ──────────────────────────────── */
        .page-header {
            margin-bottom: 1.5rem;
        }
        
        .page-title {
            font-family: var(--font-display);
            font-size: 1.75rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            color: var(--udrive-navy);
            margin-bottom: 0.25rem;
            line-height: 1.2;
        }
        
        .page-subtitle {
            font-family: var(--font-body);
            font-size: 0.9375rem;
            color: var(--udrive-text-secondary);
        }

        /* ── Top Navigation ──────────────────────────────── */
        .topnav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 64px;
            background: var(--udrive-white);
            border-bottom: 1px solid var(--udrive-border);
            display: flex;
            align-items: center;
            padding: 0 1.5rem;
            z-index: 1000;
            box-shadow: var(--shadow-sm);
        }
        
        .topnav-logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-family: var(--font-display);
            font-weight: 800;
            font-size: 1.125rem;
            color: var(--udrive-navy);
        }
        
        .topnav-logo-icon {
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, var(--udrive-violet), var(--udrive-violet-dark));
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 800;
        }
        
        .topnav-nav {
            display: flex;
            align-items: center;
            gap: 0.25rem;
            margin-left: 2.5rem;
        }
        
        .topnav-nav-item {
            padding: 0.5rem 1rem;
            border-radius: var(--radius-md);
            font-family: var(--font-display);
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--udrive-text-secondary);
            cursor: pointer;
            transition: all 0.15s ease;
        }
        
        .topnav-nav-item:hover {
            background: var(--udrive-bg-secondary);
            color: var(--udrive-text);
        }
        
        .topnav-nav-item.active {
            background: rgba(124, 58, 237, 0.1);
            color: var(--udrive-violet);
        }
        
        .topnav-user {
            margin-left: auto;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .topnav-user-avatar {
            width: 36px;
            height: 36px;
            border-radius: var(--radius-full);
            background: linear-gradient(135deg, var(--udrive-cyan), var(--udrive-violet));
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 700;
            font-size: 0.875rem;
        }
        
        .topnav-user-info {
            text-align: right;
        }
        
        .topnav-user-name {
            font-family: var(--font-display);
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--udrive-text);
        }
        
        .topnav-user-role {
            font-size: 0.75rem;
            color: var(--udrive-text-muted);
        }
        
        .topnav-user-logout {
            padding: 0.375rem 0.75rem;
            border-radius: var(--radius-md);
            font-size: 0.8125rem;
            font-weight: 600;
            border: 1px solid var(--udrive-border);
            background: var(--udrive-white);
            color: var(--udrive-text-secondary);
            cursor: pointer;
            transition: all 0.15s ease;
        }
        
        .topnav-user-logout:hover {
            background: rgba(239, 68, 68, 0.05);
            border-color: rgba(239, 68, 68, 0.3);
            color: var(--udrive-error);
        }

        /* ── Main Content Area ──────────────────────── */
        .main-content {
            padding-top: 80px;
            padding-left: 2rem;
            padding-right: 2rem;
            padding-bottom: 2rem;
        }

        /* ── Chart Container ───────────────────────────── */
        .chart-container {
            background: var(--udrive-white);
            border: 1px solid var(--udrive-border);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            box-shadow: var(--shadow-card);
        }
        
        .chart-header {
            font-family: var(--font-display);
            font-size: 1rem;
            font-weight: 700;
            color: var(--udrive-text);
            margin-bottom: 1rem;
        }

        /* ── Sparkline Mini Chart ───────────────────── */
        .sparkline {
            height: 32px;
            display: flex;
            align-items: flex-end;
            gap: 2px;
        }
        
        .sparkline-bar {
            flex: 1;
            background: linear-gradient(to top, var(--udrive-violet), var(--udrive-violet-light));
            border-radius: 2px 2px 0 0;
            opacity: 0.6;
            transition: all 0.2s ease;
        }
        
        .sparkline-bar:last-child {
            opacity: 1;
        }

        /* ── Empty State ─────────────────────────────── */
        .empty-state {
            text-align: center;
            padding: 3rem;
            color: var(--udrive-text-muted);
        }
        
        .empty-state-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            opacity: 0.5;
        }
        
        .empty-state-title {
            font-family: var(--font-display);
            font-size: 1.125rem;
            font-weight: 700;
            color: var(--udrive-text-secondary);
            margin-bottom: 0.5rem;
        }

        /* ── Filter Bar ───────────────────────────── */
        .filter-bar {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1rem 1.5rem;
            background: var(--udrive-white);
            border: 1px solid var(--udrive-border);
            border-radius: var(--radius-lg);
            margin-bottom: 1.5rem;
        }
        
        .filter-bar-label {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--udrive-text-muted);
        }

        /* ── Animations ───────────────────────────── */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-10px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        .animate-fade-in {
            animation: fadeIn 0.3s ease forwards;
        }
        
        .animate-slide-in {
            animation: slideIn 0.3s ease forwards;
        }

        /* ── Responsive ───────────────────────────── */
        @media (max-width: 768px) {
            .block-container {
                padding: 1rem !important;
            }
            
            .topnav-nav {
                display: none;
            }
            
            .main-content {
                padding: 1rem;
                padding-top: 80px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, delta: str = "", color: str = "#7C3AED", icon: str = "", sparkline_data: list = None):
    """Render a modern KPI card with trend indicator and optional sparkline."""
    delta_html = ""
    if delta:
        is_positive = delta.startswith("+") or delta.replace("%", "").replace(".", "").isdigit()
        delta_clr = "#10B981" if is_positive else "#EF4444"
        delta_class = "positive" if is_positive else "negative"
        arrow = "↑" if is_positive else "↓"
        delta_html = f'<div class="kpi-card-delta {delta_class}">{arrow} {delta}</div>'
    
    sparkline_html = ""
    if sparkline_data:
        bars = ""
        for i, v in enumerate(sparkline_data):
            bar_height = max(4, min(28, v))
            bars += f'<div class="sparkline-bar" style="height:{bar_height}px"></div>'
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


def enterprise_card(title: str, content: str = None):
    """Render an enterprise-styled card container."""
    header = f'<div class="enterprise-card-header">{title}</div>' if title else ""
    if content:
        st.markdown(f'<div class="enterprise-card">{header}{content}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="enterprise-card">{header}', unsafe_allow_html=True)


def section_header(title: str, subtitle: str = ""):
    st.markdown(
        f'''
        <div class="page-header">
            <div class="page-title">{title}</div>
            {"<div class='page-subtitle'>" + subtitle + "</div>" if subtitle else ""}
        </div>
        ''',
        unsafe_allow_html=True,
    )


def badge(text: str, kind: str = "info"):
    """Render a status badge."""
    return f'<span class="badge badge-{kind}">{text}</span>'


def chart_container(title: str = None):
    """Create a chart container wrapper."""
    header = f'<div class="chart-header">{title}</div>' if title else ""
    st.markdown(f'<div class="chart-container">{header}', unsafe_allow_html=True)


def chart_container_end():
    """Close a chart container."""
    st.markdown('</div>', unsafe_allow_html=True)


# ── Plotly Chart Styling ──────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#64748B", size=12),
    margin=dict(l=10, r=10, t=30, b=10),
    title=dict(font=dict(family="Plus Jakarta Sans", size=14, weight=700, color="#1E293B")),
)


def style_plotly_fig(fig):
    """Apply enterprise styling to a Plotly figure."""
    fig.update_layout(
        **CHART_LAYOUT,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#64748B", size=12),
        margin=dict(l=40, r=20, t=40, b=40),
        title=dict(font=dict(family="Plus Jakarta Sans", size=14, weight=700, color="#1E293B")),
        xaxis=dict(
            gridcolor="#E2E8F0",
            linecolor="#E2E8F0",
            tickfont=dict(family="Inter", size=11),
        ),
        yaxis=dict(
            gridcolor="#E2E8F0",
            linecolor="#E2E8F0",
            tickfont=dict(family="Inter", size=11),
        ),
        legend=dict(
            font=dict(family="Inter", size=11),
            bgcolor="rgba(0,0,0,0)",
        ),
        legend_title=dict(font=dict(family="Plus Jakarta Sans", size=12, weight=600)),
    )
    fig.update_traces(marker=dict(line=dict(width=0)))
    return fig