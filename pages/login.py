"""
Login Page
"""

import streamlit as st
from utils.auth import authenticate


def render_login():
    st.markdown(
        """
        <style>
        .login-wrap {
            max-width: 420px;
            margin: 6vh auto 0;
            padding: 2.5rem;
            background: var(--bg-surface);
            border: 1px solid var(--bg-border);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-card), var(--shadow-glow);
        }
        </style>
        <div class="login-wrap">
            <div style="text-align:center;margin-bottom:2rem">
                <div style="font-family:'Syne',sans-serif;font-size:2.5rem;font-weight:800;
                            letter-spacing:-0.04em;color:#F0F2FF;line-height:1">
                    QA <span style="color:#00D4FF">Pro</span>
                </div>
                <div style="font-size:0.78rem;color:#8B92B5;letter-spacing:0.12em;
                            text-transform:uppercase;margin-top:0.4rem">
                    Performance Management Platform
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col = st.columns([1, 2, 1])[1]

    with col:
        st.markdown("### Sign In")
        email = st.text_input("Email Address", placeholder="you@company.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")

        if st.button("Sign In →", use_container_width=True):
            if not email or not password:
                st.error("Please enter your email and password.")
            else:
                success, msg = authenticate(email, password)
                if success:
                    st.success("Welcome back!")
                    st.rerun()
                else:
                    st.error(msg)

        st.markdown("---")
        st.markdown(
            """
            <div style="font-size:0.78rem;color:#4A5075;text-align:center">
                <strong style="color:#8B92B5">Demo Credentials</strong><br>
                admin@qa-pro.com / Admin@123<br>
                evaluator@qa-pro.com / Eval@123<br>
                coach@qa-pro.com / Coach@123<br>
                agent@qa-pro.com / Agent@123
            </div>
            """,
            unsafe_allow_html=True,
        )
