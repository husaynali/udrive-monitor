"""
Agent Performance Dashboard
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.theme import section_header
from utils.auth import current_user, has_role

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#8B92B5", size=12),
    margin=dict(l=10, r=10, t=30, b=10),
)


def render():
    section_header("Agent Performance", "Individual and team performance tracking and risk indicators")

    from utils.auth import load_evaluations
    evals = load_evaluations()
    if not evals:
        st.info("No data yet.")
        return

    df = pd.DataFrame(evals)
    df["call_date"] = pd.to_datetime(df["call_date"])

    user = current_user()

    # Agents only see themselves
    if user.get("role") == "agent":
        df = df[df["advisor_name"] == user.get("name")]
        if df.empty:
            st.info("No evaluations found for your profile.")
            return

    # ── Agent selector (for non-agents) ───────────────────────────────────
    if has_role("super_admin","qa_admin","team_leader","ops_manager"):
        agents = sorted(df["advisor_name"].unique().tolist())
        selected_agent = st.selectbox("Select Agent", ["All Agents"] + agents)
        if selected_agent != "All Agents":
            agent_df = df[df["advisor_name"] == selected_agent]
        else:
            agent_df = df
    else:
        agent_df = df
        selected_agent = user.get("name","")

    total = len(agent_df)
    avg   = agent_df["total_score"].mean()
    pr    = agent_df["passed"].sum() / total * 100 if total else 0
    nogo  = agent_df["no_go_violation"].notna().sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Evaluations",    total)
    c2.metric("Avg Score",      f"{avg:.1f}%")
    c3.metric("Pass Rate",      f"{pr:.1f}%")
    c4.metric("No-Go Count",    nogo)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Score over time ────────────────────────────────────────────────────
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown('<div class="qa-card"><div class="qa-card-header">Score Trend</div>', unsafe_allow_html=True)
        trend = agent_df.sort_values("call_date")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trend["call_date"], y=trend["total_score"],
            mode="lines+markers",
            line=dict(color="#00D4FF", width=2),
            marker=dict(color=["#00E5A0" if p else "#FF4B6E" for p in trend["passed"]], size=8),
        ))
        fig.add_hline(y=75, line_dash="dash", line_color="rgba(255,75,110,0.5)")
        fig.update_layout(**PLOTLY_LAYOUT, height=280,
                          yaxis=dict(range=[0,105], gridcolor="#2A2E45"),
                          xaxis=dict(gridcolor="#2A2E45"))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="qa-card"><div class="qa-card-header">Risk Level</div>', unsafe_allow_html=True)

        if avg >= 85:
            risk, color, label = 85, "#00E5A0", "LOW RISK"
        elif avg >= 75:
            risk, color, label = 65, "#FFB800", "MODERATE"
        elif avg >= 60:
            risk, color, label = 45, "#FF8C00", "HIGH RISK"
        else:
            risk, color, label = 25, "#FF4B6E", "CRITICAL"

        fig2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg,
            gauge=dict(
                axis=dict(range=[0,100], tickcolor="#4A5075"),
                bar=dict(color=color),
                bgcolor="#161920",
                bordercolor="#2A2E45",
                steps=[
                    dict(range=[0,60],  color="rgba(255,75,110,0.1)"),
                    dict(range=[60,75], color="rgba(255,184,0,0.1)"),
                    dict(range=[75,100],color="rgba(0,229,160,0.1)"),
                ],
                threshold=dict(line=dict(color="#FF4B6E", width=3), thickness=0.8, value=75),
            ),
            number=dict(suffix="%", font=dict(family="Syne", color="#F0F2FF", size=28)),
        ))
        fig2.update_layout(**PLOTLY_LAYOUT, height=280)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown(
            f'<div style="text-align:center;margin-top:-1rem">'
            f'<span class="badge" style="background:rgba(0,0,0,0.3);color:{color};'
            f'border:1px solid {color}">{label}</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Evaluation history ─────────────────────────────────────────────────
    st.markdown('<div class="qa-card"><div class="qa-card-header">Evaluation History</div>', unsafe_allow_html=True)
    history = agent_df.sort_values("call_date", ascending=False)[
        ["id","advisor_name","call_date","topic","total_score","passed","no_go_violation"]
    ].copy()
    history.columns = ["ID","Agent","Date","Topic","Score","Passed","No-Go"]
    history["Score"]  = history["Score"].apply(lambda x: f"{x:.0f}%")
    history["Passed"] = history["Passed"].apply(lambda x: "✅ PASS" if x else "❌ FAIL")
    history["No-Go"]  = history["No-Go"].fillna("—")
    history["Date"]   = history["Date"].dt.strftime("%Y-%m-%d")
    st.dataframe(history, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
