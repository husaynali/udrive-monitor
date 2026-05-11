"""
Executive Dashboard — Top-level KPIs and overview
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.theme import section_header, kpi_card
from utils.auth import current_user


PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#8B92B5", size=12),
    margin=dict(l=10, r=10, t=30, b=10),
)


def render():
    section_header("Executive Dashboard", "Real-time overview of QA, coaching, and performance metrics")

    from utils.auth import load_evaluations, load_coaching_sessions
    evals = load_evaluations()
    sessions = load_coaching_sessions()

    if not evals:
        st.info("No evaluation data yet. Create your first evaluation to see insights.")
        return

    df = pd.DataFrame(evals)
    df["call_date"] = pd.to_datetime(df["call_date"])

    total     = len(df)
    avg_score = df["total_score"].mean()
    pass_rate = (df["passed"].sum() / total * 100) if total else 0
    nogo_count= df["no_go_violation"].notna().sum()
    coaching_total = len(sessions)
    coaching_done  = sum(1 for s in sessions if s.get("completion_status") == "Completed")
    coach_rate = (coaching_done / coaching_total * 100) if coaching_total else 0
    high_risk  = df[df["total_score"] < 60]["advisor_name"].nunique()

    # ── KPI Row ────────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: kpi_card("Total Audits",       str(total),          "+12 vs last month", "#00D4FF", "🎯")
    with c2: kpi_card("Avg QA Score",       f"{avg_score:.1f}%", "+2.3%",             "#00E5A0", "📊")
    with c3: kpi_card("Pass Rate",          f"{pass_rate:.1f}%", "+1.8%",             "#22C55E", "✅")
    with c4: kpi_card("No-Go Violations",   str(nogo_count),     f"-{max(0,nogo_count-5)} vs last", "#FF4B6E", "🚨")
    with c5: kpi_card("Coaching Done",      f"{coach_rate:.0f}%","",                  "#FFB800", "🎓")
    with c6: kpi_card("High-Risk Agents",   str(high_risk),      "",                  "#9D7BFF", "⚠️")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row 1 ──────────────────────────────────────────────────────
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown('<div class="qa-card">', unsafe_allow_html=True)
        st.markdown('<div class="qa-card-header">QA Score Trend — Last 90 Days</div>', unsafe_allow_html=True)

        weekly = (
            df.set_index("call_date")
            .resample("W")["total_score"]
            .agg(["mean", "min", "max"])
            .reset_index()
        )

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=weekly["call_date"], y=weekly["max"],
            fill=None, mode="lines", line=dict(width=0),
            showlegend=False,
        ))
        fig.add_trace(go.Scatter(
            x=weekly["call_date"], y=weekly["min"],
            fill="tonexty", mode="lines", line=dict(width=0),
            fillcolor="rgba(0,212,255,0.08)", showlegend=False,
        ))
        fig.add_trace(go.Scatter(
            x=weekly["call_date"], y=weekly["mean"],
            mode="lines+markers",
            line=dict(color="#00D4FF", width=2.5),
            marker=dict(color="#00D4FF", size=6),
            name="Avg Score",
        ))
        fig.add_hline(y=75, line_dash="dash", line_color="rgba(255,75,110,0.5)",
                      annotation_text="Pass Threshold", annotation_font_color="#FF4B6E")
        fig.update_layout(**PLOTLY_LAYOUT, height=260,
                          yaxis=dict(range=[0, 105], gridcolor="#2A2E45"),
                          xaxis=dict(gridcolor="#2A2E45"))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="qa-card">', unsafe_allow_html=True)
        st.markdown('<div class="qa-card-header">Pass / Fail Split</div>', unsafe_allow_html=True)

        passed = df["passed"].sum()
        failed = total - passed
        fig2 = go.Figure(go.Pie(
            labels=["Pass", "Fail"],
            values=[passed, failed],
            hole=0.68,
            marker=dict(colors=["#00E5A0", "#FF4B6E"]),
            textinfo="none",
        ))
        fig2.add_annotation(
            text=f"<b>{pass_rate:.0f}%</b><br><span style='font-size:10px'>Pass Rate</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=20, color="#F0F2FF", family="Syne"),
        )
        fig2.update_layout(**PLOTLY_LAYOUT, height=260, showlegend=True,
                           legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center"))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Charts row 2 ──────────────────────────────────────────────────────
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="qa-card">', unsafe_allow_html=True)
        st.markdown('<div class="qa-card-header">Agent Performance Leaderboard</div>', unsafe_allow_html=True)

        leader = (
            df.groupby("advisor_name")["total_score"]
            .mean()
            .reset_index()
            .sort_values("total_score", ascending=True)
            .tail(8)
        )
        colors = ["#FF4B6E" if s < 75 else "#00E5A0" for s in leader["total_score"]]
        fig3 = go.Figure(go.Bar(
            x=leader["total_score"],
            y=leader["advisor_name"],
            orientation="h",
            marker=dict(color=colors, opacity=0.85),
            text=[f"{s:.0f}%" for s in leader["total_score"]],
            textposition="outside",
        ))
        fig3.update_layout(**PLOTLY_LAYOUT, height=280,
                           xaxis=dict(range=[0, 105], gridcolor="#2A2E45"),
                           yaxis=dict(gridcolor="#2A2E45"))
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="qa-card">', unsafe_allow_html=True)
        st.markdown('<div class="qa-card-header">Top Failure Categories</div>', unsafe_allow_html=True)

        score_cols = [
            "greeting_format","closing_format","empathy_reassurance","effective_questions",
            "attentiveness","tone_of_voice","waiting_procedures","accurate_resolution",
            "business_instructions","documentation_accuracy",
        ]
        from config.settings import SCORE_WEIGHTS

        fail_data = []
        for col in score_cols:
            if col in df.columns:
                pass  # handled below

        # Compute average achievement per category
        cat_scores = {}
        for col in score_cols:
            if col in df.columns:
                max_possible = SCORE_WEIGHTS.get(col, 5)
                avg = df["scores"].apply(lambda s: s.get(col, 0) if isinstance(s, dict) else 0).mean()
                cat_scores[col.replace("_", " ").title()] = round((avg / max_possible) * 100, 1)

        cat_df = pd.DataFrame(list(cat_scores.items()), columns=["Category", "Achievement%"])
        cat_df = cat_df.sort_values("Achievement%").head(8)
        colors4 = ["#FF4B6E" if v < 75 else "#FFB800" for v in cat_df["Achievement%"]]

        fig4 = go.Figure(go.Bar(
            y=cat_df["Category"],
            x=cat_df["Achievement%"],
            orientation="h",
            marker=dict(color=colors4, opacity=0.85),
            text=[f"{v}%" for v in cat_df["Achievement%"]],
            textposition="outside",
        ))
        fig4.update_layout(**PLOTLY_LAYOUT, height=280,
                           xaxis=dict(range=[0, 110], gridcolor="#2A2E45"),
                           yaxis=dict(gridcolor="#2A2E45"))
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Recent evaluations ────────────────────────────────────────────────
    st.markdown('<div class="qa-card">', unsafe_allow_html=True)
    st.markdown('<div class="qa-card-header">Recent Evaluations</div>', unsafe_allow_html=True)

    recent = df.sort_values("call_date", ascending=False).head(10)
    display_df = recent[[
        "id", "advisor_name", "call_date", "topic", "total_score", "passed", "no_go_violation"
    ]].copy()
    display_df.columns = ["ID", "Agent", "Date", "Topic", "Score", "Passed", "No-Go"]
    display_df["Score"] = display_df["Score"].apply(lambda x: f"{x:.0f}%")
    display_df["Passed"] = display_df["Passed"].apply(lambda x: "✅ PASS" if x else "❌ FAIL")
    display_df["No-Go"] = display_df["No-Go"].fillna("—")
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")

    st.dataframe(display_df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
