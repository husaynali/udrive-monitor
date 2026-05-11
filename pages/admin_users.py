"""
Admin — User Management (Production / SQLite)
"""

import streamlit as st
import pandas as pd
from utils.theme import section_header
from utils.auth import require_auth, has_role, load_users, log_action
from utils.database import create_user, update_user_role, deactivate_user
from config.settings import ROLES, DEPARTMENTS


def render():
    require_auth()
    if not has_role("super_admin", "qa_admin"):
        st.error("Access denied.")
        return

    section_header("User Management", "Create, edit, and manage system users and their roles")

    tab1, tab2 = st.tabs(["👥 All Users", "➕ Add User"])

    with tab1:
        users = load_users()
        if not users:
            st.info("No users found.")
        else:
            df = pd.DataFrame(users)
            safe_cols = [c for c in df.columns if c not in ("password_hash",)]
            st.dataframe(df[safe_cols], use_container_width=True, hide_index=True)

            st.markdown("---")
            st.markdown("#### Edit User Role")
            ec1, ec2, ec3 = st.columns(3)
            names    = [u.get("name","") for u in users]
            sel_user = ec1.selectbox("Select User", names)
            new_role = ec2.selectbox("New Role", list(ROLES.keys()))
            if ec3.button("Update Role"):
                update_user_role(sel_user, new_role)
                log_action("USER_ROLE_UPDATED", f"Role of {sel_user} changed to {new_role}")
                st.success(f"Role updated for **{sel_user}**")
                st.rerun()

            st.markdown("---")
            st.markdown("#### Deactivate User")
            da1, da2 = st.columns(2)
            deact_name = da1.selectbox("Select User to Deactivate", names, key="deact")
            if da2.button("Deactivate", type="primary"):
                target = next((u for u in users if u["name"] == deact_name), None)
                if target:
                    deactivate_user(target["id"])
                    log_action("USER_DEACTIVATED", f"User {deact_name} deactivated")
                    st.success(f"User **{deact_name}** deactivated.")
                    st.rerun()

    with tab2:
        st.markdown("### Create New User")
        with st.form("new_user_form"):
            nc1, nc2 = st.columns(2)
            new_name     = nc1.text_input("Full Name")
            new_email    = nc2.text_input("Email")
            nc3, nc4     = st.columns(2)
            new_role     = nc3.selectbox("Role", list(ROLES.keys()))
            new_dept     = nc4.selectbox("Department", DEPARTMENTS)
            nc5, nc6     = st.columns(2)
            new_agent_id = nc5.text_input("Agent ID (optional)")
            new_password = nc6.text_input("Password", type="password", value="Changeme@1")

            if st.form_submit_button("Create User"):
                if new_name and new_email and new_password:
                    uid = create_user(new_name, new_email, new_password, new_role, new_dept, new_agent_id)
                    log_action("USER_CREATED", f"User {new_name} ({new_email}) created with role {new_role}")
                    st.success(f"User **{new_name}** created! (ID: {uid[:8]})")
                else:
                    st.error("Name, email, and password are required.")
