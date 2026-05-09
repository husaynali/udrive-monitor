"""
QA Insights Dashboard
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.theme import section_header
from config.settings import SCORE_WEIGHTS

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#8B92B5", size=12),
    margin=dict(l=10, r=10, t=30, b=10),
)


def render():
    section_header("QA Insights", "Deep analysis of quality evaluation trends and category performance")

    from utils.auth import load_evaluations
    evals = load_evaluations()
    if not evals:
        st.info("No evaluations yet.")
        return

    df = pd.DataFrame(evals)
    df["call_date"] = pd.to_datetime(df["call_date"])

    # ── Filters ───────────────────────────────────────────────────────────
    with st.expander("🔍 Filters", expanded=False):
        fc1, fc2, fc3 = st.columns(3)
        departments = ["All"] + sorted(df["department"].unique().tolist())
        teams = ["All"] + sorted(df["team_lead"].unique().tolist())
        topics = ["All"] + sorted(df["topic"].unique().tolist())

        dept_f  = fc1.selectbox("Department", departments)
        team_f  = fc2.selectbox("Team Lead",  teams)
        topic_f = fc3.selectbox("Topic",      topics)

        if dept_f  != "All": df = df[df["department"] == dept_f]
        if team_f  != "All": df = df[df["team_lead"]  == team_f]
        if topic_f != "All": df = df[df["topic"]       == topic_f]

    if df.empty:
        st.warning("No data for the selected filters.")
        return

    total     = len(df)
    avg_score = df["total_score"].mean()
    pass_rate = df["passed"].sum() / total * 100
    nogo_ct   = df["no_go_violation"].notna().sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Evaluations",   total)
    c2.metric("Average QA Score",    f"{avg_score:.1f}%")
    c3.metric("Pass Rate",           f"{pass_rate:.1f}%")
    c4.metric("No-Go Violations",    nogo_ct)

    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Score Trends", "📊 Category Analysis", "🗓️ Period Comparison", "🚨 Violations"])

    with tab1:
        weekly = df.set_index("call_date").resample("W")["total_score"].agg(["mean","min","max"]).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=weekly["call_date"], y=weekly["max"], fill=None, mode="lines",
                                  line=dict(width=0), showlegend=False))
        fig.add_trace(go.Scatter(x=weekly["call_date"], y=weekly["min"], fill="tonexty", mode="lines",
                                  line=dict(width=0), fillcolor="rgba(0,212,255,0.07)", showlegend=False))
        fig.add_trace(go.Scatter(x=weekly["call_date"], y=weekly["mean"], mode="lines+markers",
                                  line=dict(color="#00D4FF", width=2), name="Weekly Avg"))
        fig.add_hline(y=75, line_dash="dash", line_color="rgba(255,75,110,0.5)")
        fig.update_layout(**PLOTLY_LAYOUT, height=320,
                          yaxis=dict(range=[0,105], gridcolor="#2A2E45"),
                          xaxis=dict(gridcolor="#2A2E45"))
        st.plotly_chart(fig, use_container_width=True)

        # Team heatmap
        st.markdown("#### Team Performance Heatmap")
        pivot = df.pivot_table(index="advisor_name", columns="topic", values="total_score", aggfunc="mean")
        fig2 = px.imshow(
            pivot,
            color_continuous_scale=[[0,"#FF4B6E"],[0.5,"#FFB800"],[1,"#00E5A0"]],
            zmin=0, zmax=100,
            aspect="auto",
        )
        fig2.update_layout(**PLOTLY_LAYOUT, height=350)
        st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        cat_scores = {}
        for col, weight in SCORE_WEIGHTS.items():
            avg = df["scores"].apply(lambda s: s.get(col, 0) if isinstance(s, dict) else 0).mean()
            cat_scores[col.replace("_"," ").title()] = round((avg / weight) * 100, 1)

        cat_df = pd.DataFrame(list(cat_scores.items()), columns=["Category","Score%"])
        cat_df = cat_df.sort_values("Score%", ascending=True)
        colors = ["#FF4B6E" if v < 70 else "#FFB800" if v < 85 else "#00E5A0" for v in cat_df["Score%"]]

        fig3 = go.Figure(go.Bar(y=cat_df["Category"], x=cat_df["Score%"], orientation="h",
                                 marker=dict(color=colors, opacity=0.9),
                                 text=[f"{v}%" for v in cat_df["Score%"]], textposition="outside"))
        fig3.update_layout(**PLOTLY_LAYOUT, height=400, xaxis=dict(range=[0,110], gridcolor="#2A2E45"))
        st.plotly_chart(fig3, use_container_width=True)

    with tab3:
        df["month"] = df["call_date"].dt.to_period("M").astype(str)
        monthly = df.groupby("month")["total_score"].mean().reset_index()
        fig4 = go.Figure(go.Bar(
            x=monthly["month"], y=monthly["total_score"],
            marker=dict(color="#00D4FF", opacity=0.8),
            text=[f"{v:.0f}%" for v in monthly["total_score"]], textposition="outside",
        ))
        fig4.add_hline(y=75, line_dash="dash", line_color="rgba(255,75,110,0.6)")
        fig4.update_layout(**PLOTLY_LAYOUT, height=320, yaxis=dict(range=[0,105], gridcolor="#2A2E45"))
        st.plotly_chart(fig4, use_container_width=True)

    with tab4:
        nogo_df = df[df["no_go_violation"].notna()]
        if nogo_df.empty:
            st.success("🎉 No No-Go violations in selected period!")
        else:
            counts = nogo_df["no_go_violation"].value_counts().reset_index()
            counts.columns = ["Violation", "Count"]
            fig5 = go.Figure(go.Bar(
                y=counts["Violation"], x=counts["Count"], orientation="h",
                marker=dict(color="#FF4B6E", opacity=0.85),
                text=counts["Count"], textposition="outside",
            ))
            fig5.update_layout(**PLOTLY_LAYOUT, height=280)
            st.plotly_chart(fig5, use_container_width=True)

            st.dataframe(
                nogo_df[["id","advisor_name","call_date","no_go_violation","total_score"]]
                .rename(columns={"id":"ID","advisor_name":"Agent","call_date":"Date",
                                 "no_go_violation":"Violation","total_score":"Score"}),
                use_container_width=True, hide_index=True,
            )
