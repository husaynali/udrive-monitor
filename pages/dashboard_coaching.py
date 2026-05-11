"""
Coaching Insights Dashboard
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.theme import section_header

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#8B92B5", size=12),
    margin=dict(l=10, r=10, t=30, b=10),
)


def render():
    section_header("Coaching Insights", "Coaching effectiveness, completion rates, and improvement tracking")

    from utils.auth import load_coaching_sessions
    sessions = load_coaching_sessions()
    if not sessions:
        st.info("No coaching sessions yet.")
        return

    df = pd.DataFrame(sessions)

    total    = len(df)
    completed = (df["completion_status"] == "Completed").sum()
    pending  = (df["completion_status"] == "Pending Agent").sum()
    progress = (df["completion_status"] == "In Progress").sum()
    comp_rate = completed / total * 100 if total else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Sessions",        total)
    c2.metric("Completed",             completed)
    c3.metric("In Progress",           progress)
    c4.metric("Completion Rate",       f"{comp_rate:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Coaching status funnel
        st.markdown('<div class="qa-card"><div class="qa-card-header">Coaching Completion Funnel</div>', unsafe_allow_html=True)
        status_counts = df["completion_status"].value_counts()
        fig = go.Figure(go.Funnel(
            y=status_counts.index.tolist(),
            x=status_counts.values.tolist(),
            marker=dict(color=["#00E5A0","#00D4FF","#FFB800","#FF4B6E","#9D7BFF"]),
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=280)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Coaching types
        st.markdown('<div class="qa-card"><div class="qa-card-header">Coaching Types Distribution</div>', unsafe_allow_html=True)
        type_counts = df["coaching_type"].value_counts()
        fig2 = go.Figure(go.Pie(
            labels=type_counts.index.tolist(),
            values=type_counts.values.tolist(),
            hole=0.55,
            marker=dict(colors=["#00D4FF","#FF4B6E","#00E5A0","#FFB800","#9D7BFF","#06B6D4"]),
            textinfo="label+percent",
        ))
        fig2.update_layout(**PLOTLY_LAYOUT, height=280, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Most coached agents
    st.markdown('<div class="qa-card"><div class="qa-card-header">Most Coached Agents</div>', unsafe_allow_html=True)
    agent_counts = df["advisor_name"].value_counts().reset_index().head(10)
    agent_counts.columns = ["Agent", "Sessions"]
    fig3 = go.Figure(go.Bar(
        x=agent_counts["Agent"], y=agent_counts["Sessions"],
        marker=dict(color="#9D7BFF", opacity=0.85),
        text=agent_counts["Sessions"], textposition="outside",
    ))
    fig3.update_layout(**PLOTLY_LAYOUT, height=260, yaxis=dict(gridcolor="#2A2E45"))
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Recent sessions table
    st.markdown('<div class="qa-card"><div class="qa-card-header">Recent Coaching Sessions</div>', unsafe_allow_html=True)
    display = df[["id","advisor_name","coaching_date","coaching_type","status","completion_status","qa_score"]].copy()
    display.columns = ["ID","Agent","Date","Type","Status","Completion","QA Score"]
    display["QA Score"] = display["QA Score"].apply(lambda x: f"{x:.0f}%")
    st.dataframe(display.head(15), use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
