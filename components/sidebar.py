"""
Sidebar Navigation Component
"""

import streamlit as st
from utils.auth import current_user, logout, has_role
from config.settings import ROLES


NAV_STRUCTURE = [
    {
        "group": "📊 Dashboards",
        "items": [
            ("Executive Dashboard",  "🏠", ["super_admin","qa_admin","qa_evaluator","team_leader","ops_manager","viewer"]),
            ("QA Insights",          "🔍", ["super_admin","qa_admin","qa_evaluator","team_leader","ops_manager","viewer"]),
            ("Coaching Insights",    "🎯", ["super_admin","qa_admin","team_leader","coach","ops_manager","viewer"]),
            ("Agent Performance",    "👤", ["super_admin","qa_admin","team_leader","ops_manager","agent","viewer"]),
            ("Root Cause Analysis",  "🔬", ["super_admin","qa_admin","ops_manager"]),
        ],
    },
    {
        "group": "📋 Evaluations",
        "items": [
            ("New Evaluation",    "➕", ["super_admin","qa_admin","qa_evaluator"]),
            ("Evaluations List",  "📝", ["super_admin","qa_admin","qa_evaluator","team_leader","ops_manager"]),
        ],
    },
    {
        "group": "🎓 Coaching",
        "items": [
            ("New Coaching Session", "➕", ["super_admin","qa_admin","team_leader","coach"]),
            ("Coaching Sessions",    "📚", ["super_admin","qa_admin","team_leader","coach","ops_manager"]),
        ],
    },
    {
        "group": "📈 Reports",
        "items": [
            ("Reports & Export", "📥", ["super_admin","qa_admin","qa_evaluator","team_leader","ops_manager","viewer"]),
        ],
    },
    {
        "group": "⚙️ Administration",
        "items": [
            ("User Management",  "👥", ["super_admin","qa_admin"]),
            ("Form Builder",     "🔧", ["super_admin","qa_admin"]),
            ("System Settings",  "⚙️",  ["super_admin"]),
            ("Audit Logs",       "🔒", ["super_admin","qa_admin"]),
        ],
    },
]


def render_sidebar() -> str:
    user = current_user()
    role = user.get("role", "viewer")
    role_cfg = ROLES.get(role, {})

    with st.sidebar:
        # ── Brand ──────────────────────────────────────────────────────────
        st.markdown(
            f"""
            <div style="padding:1rem 0 1.25rem">
                <div style="font-family:'Syne',sans-serif;font-size:1.35rem;font-weight:800;
                            letter-spacing:-0.03em;color:#F0F2FF;line-height:1">
                    QA <span style="color:#00D4FF">Pro</span>
                </div>
                <div style="font-size:0.7rem;color:#8B92B5;letter-spacing:0.1em;
                            text-transform:uppercase;margin-top:0.2rem">
                    Performance Platform
                </div>
            </div>
            <hr style="border-color:#2A2E45;margin:0 0 1rem">
            """,
            unsafe_allow_html=True,
        )

        # ── User card ──────────────────────────────────────────────────────
        role_color = role_cfg.get("color", "#8B92B5")
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:0.75rem;
                        background:#1E2130;border-radius:10px;padding:0.65rem 0.85rem;
                        margin-bottom:1.25rem;border:1px solid #2A2E45">
                <div style="width:36px;height:36px;border-radius:50%;
                            background:{role_color};display:flex;align-items:center;
                            justify-content:center;font-family:'Syne',sans-serif;
                            font-size:0.82rem;font-weight:800;color:#000;flex-shrink:0">
                    {user.get('avatar','?')}
                </div>
                <div style="min-width:0">
                    <div style="font-family:'Syne',sans-serif;font-size:0.85rem;
                                font-weight:700;color:#F0F2FF;white-space:nowrap;
                                overflow:hidden;text-overflow:ellipsis">
                        {user.get('name','—')}
                    </div>
                    <div style="font-size:0.7rem;color:{role_color};
                                text-transform:uppercase;letter-spacing:0.07em">
                        {role_cfg.get('label', role)}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Navigation ─────────────────────────────────────────────────────
        current = st.session_state.get("current_page", "Executive Dashboard")
        selected = current

        for group in NAV_STRUCTURE:
            visible = [(label, icon) for label, icon, roles in group["items"]
                       if role in roles or role == "super_admin"]
            if not visible:
                continue

            st.markdown(
                f"""<div style="font-size:0.65rem;font-weight:700;letter-spacing:0.12em;
                               text-transform:uppercase;color:#4A5075;
                               padding:0.6rem 0 0.35rem;font-family:'Syne',sans-serif">
                       {group['group']}
                   </div>""",
                unsafe_allow_html=True,
            )

            for label, icon in visible:
                is_active = label == current
                btn_style = (
                    "background:rgba(0,212,255,0.1);color:#00D4FF;"
                    "border-left:3px solid #00D4FF;padding-left:calc(0.75rem - 3px);"
                    if is_active else
                    "color:#8B92B5;"
                )
                clicked = st.button(
                    f"{icon}  {label}",
                    key=f"nav_{label}",
                    use_container_width=True,
                )
                if clicked:
                    selected = label
                    st.session_state.current_page = label

        st.markdown("<div style='flex:1'></div>", unsafe_allow_html=True)
        st.markdown("---")

        # ── Logout ─────────────────────────────────────────────────────────
        if st.button("🚪  Sign Out", use_container_width=True, type="secondary"):
            logout()

        st.markdown(
            "<div style='font-size:0.65rem;color:#4A5075;text-align:center;"
            "padding-top:0.5rem;font-family:var(--font-mono)'>v2.0.0 · QA Pro</div>",
            unsafe_allow_html=True,
        )

    return st.session_state.get("current_page", "Executive Dashboard")
