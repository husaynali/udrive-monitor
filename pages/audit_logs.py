"""
Audit Logs — Production (SQLite)
"""

import streamlit as st
import pandas as pd
from utils.theme import section_header
from utils.auth import require_auth, has_role, load_audit_logs


def render():
    require_auth()
    if not has_role("super_admin", "qa_admin"):
        st.error("Access denied.")
        return

    section_header("Audit Logs", "Complete history of all user actions, changes, and system events")

    logs = load_audit_logs()
    if not logs:
        st.info("No audit events yet.")
        return

    df = pd.DataFrame(logs)
    df.rename(columns={"user_name": "user", "user_role": "role",
                        "ip_address": "ip", "session_id": "session"}, inplace=True)

    with st.expander("🔍 Filter Logs", expanded=False):
        fc1, fc2 = st.columns(2)
        users   = ["All"] + sorted(df["user"].unique().tolist())
        actions = ["All"] + sorted(df["action"].unique().tolist())
        user_f   = fc1.selectbox("User",   users)
        action_f = fc2.selectbox("Action", actions)

    filtered = df.copy()
    if user_f   != "All": filtered = filtered[filtered["user"]   == user_f]
    if action_f != "All": filtered = filtered[filtered["action"] == action_f]

    st.markdown(f"**{len(filtered)}** log entries")

    display = filtered.sort_values("timestamp", ascending=False)[[
        "id","timestamp","user","role","action","detail","ip"
    ]]
    st.dataframe(display, use_container_width=True, hide_index=True)

    csv = display.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Export Audit Log", csv, "audit_log.csv", "text/csv")
