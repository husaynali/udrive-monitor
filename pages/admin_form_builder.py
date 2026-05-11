"""
Admin — QA Form Builder
"""

import streamlit as st
from utils.theme import section_header
from utils.auth import require_auth, has_role
from config.settings import SCORE_WEIGHTS, NO_GO_VIOLATIONS


def render():
    require_auth()
    if not has_role("super_admin", "qa_admin"):
        st.error("Access denied.")
        return

    section_header("QA Form Builder", "Configure scoring weights, categories, and No-Go rules")

    tab1, tab2, tab3 = st.tabs(["⚖️ Score Weights", "🚨 No-Go Rules", "📋 Category Config"])

    with tab1:
        st.markdown("### Configure Scoring Weights")
        st.info("Adjust category weights. Total must equal 100%.")

        weights = dict(SCORE_WEIGHTS)  # copy
        total_w = 0
        new_weights = {}

        for key, val in weights.items():
            label = key.replace("_"," ").title()
            c1, c2 = st.columns([3,1])
            new_val = c1.slider(label, 0, 30, val, key=f"w_{key}")
            c2.markdown(f"<div style='padding-top:1.4rem;color:#00D4FF;font-family:var(--font-mono)'>{new_val}%</div>", unsafe_allow_html=True)
            new_weights[key] = new_val
            total_w += new_val

        color = "#00E5A0" if total_w == 100 else "#FF4B6E"
        st.markdown(
            f"<div style='font-family:var(--font-display);font-size:1.1rem;color:{color};padding:0.5rem'>"
            f"Total: <strong>{total_w}%</strong> {'✅' if total_w == 100 else '⚠️ Must equal 100%'}</div>",
            unsafe_allow_html=True,
        )

        if st.button("Save Weights") and total_w == 100:
            st.success("Weights saved (session only — connect to DB for persistence).")

    with tab2:
        st.markdown("### No-Go Violation Rules")
        st.warning("Any of the following violations trigger automatic FAIL and coaching requirement.")

        for v in NO_GO_VIOLATIONS:
            c1, c2 = st.columns([4,1])
            c1.markdown(f"🚨 **{v}**")
            c2.toggle("Active", value=True, key=f"nogo_{v}")

        st.markdown("---")
        st.markdown("#### Add Custom No-Go Rule")
        new_rule = st.text_input("New violation name")
        if st.button("Add Rule") and new_rule:
            st.success(f"Rule **{new_rule}** added (session only).")

    with tab3:
        st.markdown("### Evaluation Categories")
        categories = [
            ("Greeting & Closing",           "C", True),
            ("Engagement & Interaction",      "D", True),
            ("Call Handling & Hold Etiquette","E", True),
            ("Typing & Language",             "F", True),
            ("Resolution Quality",            "G", True),
            ("Compliance & Verification",     "H", True),
            ("Business Instructions & Docs",  "I", True),
        ]
        for name, section, enabled in categories:
            c1, c2, c3 = st.columns([1, 4, 1])
            c1.markdown(f"**{section}**")
            c2.markdown(name)
            c3.toggle("", value=enabled, key=f"cat_{section}")

        if st.button("Save Category Config"):
            st.success("Category configuration saved.")
