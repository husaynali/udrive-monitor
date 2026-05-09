"""
Login Page - UDrive Monitor
"""

import streamlit as st
from utils.auth import authenticate


def render_login():
    st.markdown(
        """
        <div class="login-page">
            <div class="login-card">
                <div style="text-align:center;margin-bottom:1.5rem">
                    <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:2rem;font-weight:800;color:#F8FAFC;letter-spacing:-0.03em">
                        UD<span style="color:#00D4FF">rive</span> Monitor
                    </div>
                    <div style="font-size:0.8rem;color:#64748B;letter-spacing:0.1em;text-transform:uppercase;margin-top:0.5rem">
                        Performance Management Platform
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    with st.container():
        col = st.columns([1, 2, 1])[1]
        with col:
            st.markdown("### Sign In")
            email = st.text_input("Email Address", placeholder="you@company.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")

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
