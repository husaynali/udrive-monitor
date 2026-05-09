"""
Root Cause Analysis Dashboard
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.theme import section_header

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#8B92B5", size=12),
    margin=dict(l=10, r=10, t=40, b=10),
)


def render():
    section_header("Root Cause Analysis", "Pareto analysis, failure treemaps, and trend correlations")

    evals    = st.session_state.get("evaluations", [])
    sessions = st.session_state.get("coaching_sessions", [])

    if not evals:
        st.info("No data available.")
        return

    df = pd.DataFrame(evals)
    failed_df = df[~df["passed"]]

    st.markdown('<div class="qa-card"><div class="qa-card-header">Pareto — Top Failure Categories</div>', unsafe_allow_html=True)
    from config.settings import SCORE_WEIGHTS

    fail_cats = {}
    for col, weight in SCORE_WEIGHTS.items():
        failed_count = failed_df["scores"].apply(
            lambda s: 1 if isinstance(s, dict) and s.get(col, weight) < weight * 0.75 else 0
        ).sum()
        fail_cats[col.replace("_"," ").title()] = failed_count

    pareto = pd.DataFrame(list(fail_cats.items()), columns=["Category","Failures"])
    pareto = pareto.sort_values("Failures", ascending=False)
    pareto["Cumulative%"] = pareto["Failures"].cumsum() / pareto["Failures"].sum() * 100

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=pareto["Category"], y=pareto["Failures"],
        marker=dict(color="#FF4B6E", opacity=0.85),
        name="Failures", yaxis="y1",
    ))
    fig.add_trace(go.Scatter(
        x=pareto["Category"], y=pareto["Cumulative%"],
        mode="lines+markers", line=dict(color="#00D4FF", width=2),
        name="Cumulative %", yaxis="y2",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT, height=340,
        yaxis=dict(title="Failures", gridcolor="#2A2E45"),
        yaxis2=dict(title="Cumulative %", overlaying="y", side="right", range=[0,110]),
        legend=dict(orientation="h", y=1.05),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Treemap
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="qa-card"><div class="qa-card-header">Failure Treemap by Agent & Topic</div>', unsafe_allow_html=True)
        fail_grp = failed_df.groupby(["advisor_name","topic"]).size().reset_index(name="Count")
        fig2 = px.treemap(
            fail_grp, path=["advisor_name","topic"], values="Count",
            color="Count",
            color_continuous_scale=[[0,"#1E2130"],[0.5,"#FFB800"],[1,"#FF4B6E"]],
        )
        fig2.update_layout(**PLOTLY_LAYOUT, height=320)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="qa-card"><div class="qa-card-header">No-Go Violations Breakdown</div>', unsafe_allow_html=True)
        nogo_df = df[df["no_go_violation"].notna()]
        if nogo_df.empty:
            st.success("No violations recorded.")
        else:
            nogo_counts = nogo_df["no_go_violation"].value_counts().reset_index()
            nogo_counts.columns = ["Violation","Count"]
            fig3 = go.Figure(go.Pie(
                labels=nogo_counts["Violation"], values=nogo_counts["Count"],
                hole=0.5,
                marker=dict(colors=["#FF4B6E","#FF8C00","#FFB800","#9D7BFF","#00D4FF"]),
            ))
            fig3.update_layout(**PLOTLY_LAYOUT, height=320, showlegend=True,
                               legend=dict(orientation="v", x=1.01))
            st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Root causes from coaching sessions
    if sessions:
        st.markdown('<div class="qa-card"><div class="qa-card-header">Root Cause Frequency (from Coaching Sessions)</div>', unsafe_allow_html=True)
        rc_counts: dict = {}
        for s in sessions:
            for rc in s.get("root_causes", []):
                rc_counts[rc] = rc_counts.get(rc, 0) + 1

        if rc_counts:
            rc_df = pd.DataFrame(list(rc_counts.items()), columns=["Cause","Count"]).sort_values("Count", ascending=True)
            fig4 = go.Figure(go.Bar(
                y=rc_df["Cause"], x=rc_df["Count"], orientation="h",
                marker=dict(color="#9D7BFF", opacity=0.85),
                text=rc_df["Count"], textposition="outside",
            ))
            fig4.update_layout(**PLOTLY_LAYOUT, height=300)
            st.plotly_chart(fig4, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
