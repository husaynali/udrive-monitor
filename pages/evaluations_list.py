"""
Evaluations List — Production (reads from SQLite)
"""

import streamlit as st
import pandas as pd
from utils.theme import section_header
from utils.auth import load_evaluations


def render():
    section_header("Evaluations", "Browse, search, and manage all QA evaluations")

    evals = load_evaluations()
    if not evals:
        st.info("No evaluations yet. Create one via 'New Evaluation'.")
        return

    df = pd.DataFrame(evals)
    df["call_date"] = pd.to_datetime(df["call_date"])

    with st.expander("🔍 Search & Filter", expanded=True):
        fc1, fc2, fc3, fc4 = st.columns(4)
        agents   = ["All"] + sorted(df["advisor_name"].unique().tolist())
        teams    = ["All"] + sorted(df["team_lead"].unique().tolist())
        topics   = ["All"] + sorted(df["topic"].unique().tolist())
        statuses = ["All", "Pass", "Fail", "No-Go"]

        agent_f  = fc1.selectbox("Agent",  agents)
        team_f   = fc2.selectbox("Team",   teams)
        topic_f  = fc3.selectbox("Topic",  topics)
        status_f = fc4.selectbox("Status", statuses)

        dc1, dc2 = st.columns(2)
        min_date = df["call_date"].min().date()
        max_date = df["call_date"].max().date()
        from_dt = dc1.date_input("From Date", value=min_date)
        to_dt   = dc2.date_input("To Date",   value=max_date)

    filtered = df.copy()
    if agent_f  != "All": filtered = filtered[filtered["advisor_name"] == agent_f]
    if team_f   != "All": filtered = filtered[filtered["team_lead"]    == team_f]
    if topic_f  != "All": filtered = filtered[filtered["topic"]        == topic_f]
    if status_f == "Pass":  filtered = filtered[filtered["passed"]]
    elif status_f == "Fail":  filtered = filtered[~filtered["passed"] & filtered["no_go_violation"].isna()]
    elif status_f == "No-Go": filtered = filtered[filtered["no_go_violation"].notna()]
    filtered = filtered[
        (filtered["call_date"].dt.date >= from_dt) &
        (filtered["call_date"].dt.date <= to_dt)
    ]

    st.markdown(f"**{len(filtered)}** evaluations found")

    display = filtered.sort_values("call_date", ascending=False)[[
        "id","advisor_name","call_date","audit_type","topic","subtopic",
        "total_score","passed","no_go_violation","coaching_required","qa_evaluator"
    ]].copy()
    display.columns = [
        "ID","Agent","Date","Audit Type","Topic","Sub Topic",
        "Score","Passed","No-Go","Coaching?","Evaluator"
    ]
    display["Score"]     = display["Score"].apply(lambda x: f"{x:.0f}%")
    display["Passed"]    = display["Passed"].apply(lambda x: "✅ PASS" if x else "❌ FAIL")
    display["Coaching?"] = display["Coaching?"].apply(lambda x: "Yes" if x else "No")
    display["No-Go"]     = display["No-Go"].fillna("—")
    display["Date"]      = display["Date"].dt.strftime("%Y-%m-%d")

    st.dataframe(display, use_container_width=True, hide_index=True)

    csv = display.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Export to CSV", data=csv,
                       file_name="qa_evaluations_export.csv", mime="text/csv")
