"""
Coaching Sessions List — Production (SQLite)
"""

import streamlit as st
import pandas as pd
from utils.theme import section_header
from utils.auth import load_coaching_sessions


def render():
    section_header("Coaching Sessions", "Browse and manage all coaching sessions")

    sessions = load_coaching_sessions()
    if not sessions:
        st.info("No coaching sessions yet.")
        return

    df = pd.DataFrame(sessions)
    df["coaching_date"] = pd.to_datetime(df["coaching_date"])

    with st.expander("🔍 Filter", expanded=True):
        fc1, fc2, fc3 = st.columns(3)
        agents   = ["All"] + sorted(df["advisor_name"].unique().tolist())
        statuses = ["All"] + sorted(df["completion_status"].unique().tolist())
        types    = ["All"] + sorted(df["coaching_type"].unique().tolist())
        agent_f  = fc1.selectbox("Agent",  agents)
        status_f = fc2.selectbox("Status", statuses)
        type_f   = fc3.selectbox("Type",   types)

    filtered = df.copy()
    if agent_f  != "All": filtered = filtered[filtered["advisor_name"]    == agent_f]
    if status_f != "All": filtered = filtered[filtered["completion_status"]== status_f]
    if type_f   != "All": filtered = filtered[filtered["coaching_type"]    == type_f]

    st.markdown(f"**{len(filtered)}** sessions found")

    display = filtered.sort_values("coaching_date", ascending=False)[[
        "id","advisor_name","coaching_date","coaching_type","completion_status",
        "qa_score","topic","coach_name","follow_up_date"
    ]].copy()
    display.columns = ["ID","Agent","Date","Type","Status","QA Score","Topic","Coach","Follow-Up"]
    display["QA Score"] = display["QA Score"].apply(lambda x: f"{x:.0f}%")
    display["Date"]     = display["Date"].dt.strftime("%Y-%m-%d")

    st.dataframe(display, use_container_width=True, hide_index=True)

    csv = display.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Export to CSV", csv, "coaching_sessions.csv", "text/csv")
