"""
Login Page - Udrive Branding
"""

import streamlit as st
from utils.auth import authenticate


def render_login():
    st.markdown(
        """
        <style>
        .login-wrap {
            max-width: 420px;
            margin: 8vh auto 0;
            padding: 2.5rem;
            background: #FFFFFF;
            border: 1px solid #E3EBF1;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        }
        </style>
        <div class="login-wrap">
            <div style="text-align:center;margin-bottom:2rem">
                <div style="font-family:'Outfit',sans-serif;font-size:2.5rem;font-weight:800;
                            letter-spacing:-0.04em;color:#0F172A;line-height:1">
                    Udrive <span style="color:#52BAEF">Pro</span>
                </div>
                <div style="font-family:'Plus+Jakarta+Sans',sans-serif;font-size:0.78rem;color:#475569;letter-spacing:0.12em;
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
            <div style="font-size:0.78rem;color:#94A3B8;text-align:center">
                <strong style="color:#475569">Demo Credentials</strong><br>
                admin@qa-pro.com / Admin@123<br>
                evaluator@qa-pro.com / Eval@123<br>
                coach@qa-pro.com / Coach@123<br>
                agent@qa-pro.com / Agent@123
            </div>
            """,
            unsafe_allow_html=True,
        )
