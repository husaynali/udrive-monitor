"""
Executive Dashboard — Top-level KPIs and overview
Redesigned with U-Drive Enterprise UI
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.theme import section_header, kpi_card, chart_container, chart_container_end
from utils.auth import current_user
from config.settings import APP_CONFIG


PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#64748B", size=12),
    margin=dict(l=10, r=10, t=30, b=10),
)


def render():
    section_header("Executive Dashboard", "Real-time overview of QA, coaching, and performance metrics")

    from utils.auth import load_evaluations, load_coaching_sessions
    evals = load_evaluations()
    sessions = load_coaching_sessions()

    if not evals:
        # Empty state
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-state-icon">📊</div>
                <div class="empty-state-title">No evaluation data yet</div>
                <p>Create your first evaluation to see insights.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
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
    
    # Calculate trends (compare with previous period)
    # For demo, we'll use mock data - in production would compare with historical data
    recent_total = total
    total_trend = "+12%" if total > 50 else "+5%"
    score_trend = "+2.3%"
    pass_trend = "+1.8%"
    nogo_trend = f"-{max(0, nogo_count - 2)}"
    coach_trend = "+8%"
    
    # Generate sparkline data (mock data for demo)
    sparkline_scores = [65, 72, 68, 75, 78, 82, 79, 85, 88, 82, 86, 90]
    sparkline_pass = [70, 72, 75, 73, 78, 80, 82, 79, 85, 88, 86, 90]

    # ── KPI Row ────────────────────────────────────────────────────────────
    st.markdown("### Key Metrics")
    
    kpi_cols = st.columns(6)
    with kpi_cols[0]:
        kpi_card(
            "Total Audits", 
            str(total), 
            total_trend, 
            "#7C3AED", 
            "🎯",
            sparkline_scores
        )
    with kpi_cols[1]:
        kpi_card(
            "Avg QA Score", 
            f"{avg_score:.1f}%", 
            score_trend, 
            "#10B981", 
            "📊",
            sparkline_pass
        )
    with kpi_cols[2]:
        kpi_card(
            "Pass Rate", 
            f"{pass_rate:.1f}%", 
            pass_trend, 
            "#22C55E", 
            "✅",
            sparkline_pass
        )
    with kpi_cols[3]:
        kpi_card(
            "No-Go Violations", 
            str(nogo_count), 
            nogo_trend, 
            "#EF4444", 
            "🚨"
        )
    with kpi_cols[4]:
        kpi_card(
            "Coaching Done", 
            f"{coach_rate:.0f}%",
            coach_trend,
            "#F59E0B", 
            "🎓"
        )
    with kpi_cols[5]:
        kpi_card(
            "High-Risk Agents", 
            str(high_risk), 
            "", 
            "#8B5CF6", 
            "⚠️"
        )

    st.markdown("---")

    # ── Charts row 1 ──────────────────────────────────────────────────────
    col_left, col_right = st.columns([2, 1])

    with col_left:
        chart_container("QA Score Trend — Last 90 Days")

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
            fillcolor="rgba(124, 58, 237, 0.08)", showlegend=False,
        ))
        fig.add_trace(go.Scatter(
            x=weekly["call_date"], y=weekly["mean"],
            mode="lines+markers",
            line=dict(color="#7C3AED", width=2.5),
            marker=dict(color="#7C3AED", size=6),
            name="Avg Score",
        ))
        fig.add_hline(y=75, line_dash="dash", line_color="rgba(239, 68, 68, 0.5)",
                      annotation_text="Pass Threshold", annotation_font_color="#EF4444")
        fig.update_layout(
            **PLOTLY_LAYOUT, height=260,
            yaxis=dict(range=[0, 105], gridcolor="#E2E8F0"),
            xaxis=dict(gridcolor="#E2E8F0"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)
        chart_container_end()

    with col_right:
        chart_container("Pass / Fail Split")

        passed = df["passed"].sum()
        failed = total - passed
        fig2 = go.Figure(go.Pie(
            labels=["Pass", "Fail"],
            values=[passed, failed],
            hole=0.68,
            marker=dict(colors=["#10B981", "#EF4444"]),
            textinfo="none",
        ))
        fig2.add_annotation(
            text=f"<b>{pass_rate:.0f}%</b><br><span style='font-size:10px'>Pass Rate</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=20, color="#1E293B", family="Plus Jakarta Sans"),
        )
        fig2.update_layout(
            **PLOTLY_LAYOUT, height=260, showlegend=True,
            legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig2, use_container_width=True)
        chart_container_end()

    # ── Charts row 2 ──────────────────────────────────────────────────────
    col_a, col_b = st.columns(2)

    with col_a:
        chart_container("Agent Performance Leaderboard")

        leader = (
            df.groupby("advisor_name")["total_score"]
            .mean()
            .reset_index()
            .sort_values("total_score", ascending=True)
            .tail(8)
        )
        colors = ["#EF4444" if s < 75 else "#10B981" for s in leader["total_score"]]
        fig3 = go.Figure(go.Bar(
            x=leader["total_score"],
            y=leader["advisor_name"],
            orientation="h",
            marker=dict(color=colors, opacity=0.85),
            text=[f"{s:.0f}%" for s in leader["total_score"]],
            textposition="outside",
        ))
        fig3.update_layout(
            **PLOTLY_LAYOUT, height=280,
            xaxis=dict(range=[0, 105], gridcolor="#E2E8F0"),
            yaxis=dict(gridcolor="#E2E8F0"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig3, use_container_width=True)
        chart_container_end()

    with col_b:
        chart_container("Top Failure Categories")

        score_cols = [
            "greeting_format","closing_format","empathy_reassurance","effective_questions",
            "attentiveness","tone_of_voice","waiting_procedures","accurate_resolution",
            "business_instructions","documentation_accuracy",
        ]
        from config.settings import SCORE_WEIGHTS

        # Compute average achievement per category
        cat_scores = {}
        for col in score_cols:
            if col in df.columns:
                max_possible = SCORE_WEIGHTS.get(col, 5)
                avg = df["scores"].apply(lambda s: s.get(col, 0) if isinstance(s, dict) else 0).mean()
                cat_scores[col.replace("_", " ").title()] = round((avg / max_possible) * 100, 1)

        cat_df = pd.DataFrame(list(cat_scores.items()), columns=["Category", "Achievement%"])
        cat_df = cat_df.sort_values("Achievement%").head(8)
        colors4 = ["#EF4444" if v < 75 else "#F59E0B" for v in cat_df["Achievement%"]]

        fig4 = go.Figure(go.Bar(
            y=cat_df["Category"],
            x=cat_df["Achievement%"],
            orientation="h",
            marker=dict(color=colors4, opacity=0.85),
            text=[f"{v}%" for v in cat_df["Achievement%"]],
            textposition="outside",
        ))
        fig4.update_layout(
            **PLOTLY_LAYOUT, height=280,
            xaxis=dict(range=[0, 110], gridcolor="#E2E8F0"),
            yaxis=dict(gridcolor="#E2E8F0"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig4, use_container_width=True)
        chart_container_end()

    # ── AI Insights Section ────────────────────────────────────────────────
    st.markdown("### AI Insights")
    
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        chart_container("Performance Insights")
        
        # Generate AI-style insights
        insights = []
        
        if avg_score < 75:
            insights.append("⚠️ Average QA score is below the pass threshold (75%)")
        if pass_rate < 80:
            insights.append(f"📉 Pass rate dropped {100 - pass_rate:.1f}% below target")
        if nogo_count > 3:
            insights.append("🚨 Multiple No-Go violations detected this period")
        if high_risk > 0:
            insights.append(f"👤 {high_risk} agents require immediate coaching")
        
        # Calculate week-over-week change
        recent_week = df[df["call_date"] >= df["call_date"].max() - pd.Timedelta(days=7)]
        prev_week = df[(df["call_date"] < df["call_date"].max() - pd.Timedelta(days=7)) & 
                   (df["call_date"] >= df["call_date"].max() - pd.Timedelta(days=14))]
        
        if len(recent_week) > 0 and len(prev_week) > 0:
            recent_avg = recent_week["total_score"].mean()
            prev_avg = prev_week["total_score"].mean()
            change = recent_avg - prev_avg
            
            if change > 3:
                insights.append(f"📈 Score improved by {change:.1f}% this week!")
            elif change < -3:
                insights.append(f"📉 Score dropped by {abs(change):.1f}% this week")
        
        if not insights:
            insights.append("✅ All metrics look healthy!")
        
        for insight in insights:
            st.markdown(f"- {insight}")
        
        chart_container_end()
        
    with insights_col2:
        chart_container("Quick Actions")
        
        st.markdown("- 📝 Schedule coaching for low-performing agents")
        st.markdown("- 🔄 Review failed evaluations")
        st.markdown("- 📅 Set team quality targets")
        st.markdown("- 👥 Request agent feedback")
        
        chart_container_end()

    # ── Recent evaluations ────────────────────────────────────────────────
    st.markdown("### Recent Evaluations")
    
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
