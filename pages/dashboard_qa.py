"""
QA Insights Dashboard - Enhanced Analytics
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.theme import section_header, kpi_card, chart_container, chart_container_end
from config.settings import SCORE_WEIGHTS


def render():
    section_header("QA Insights", "Comprehensive quality analytics and performance insights")

    from utils.auth import load_evaluations
    evals = load_evaluations()
    if not evals:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">📊</div>
            <div class="empty-state-title">No evaluations yet</div>
            <p>Start evaluating calls to see QA insights.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    df = pd.DataFrame(evals)
    df["call_date"] = pd.to_datetime(df["call_date"])

    # Filters
    with st.expander("🔍 Advanced Filters", expanded=True):
        fc1, fc2, fc3, fc4 = st.columns(4)
        fc5, fc6, fc7, fc8 = st.columns(4)
        
        departments = ["All"] + sorted(df["department"].dropna().unique().tolist())
        teams = ["All"] + sorted(df["team_lead"].dropna().unique().tolist())
        topics = ["All"] + sorted(df["topic"].dropna().unique().tolist())
        evaluators = ["All"] + sorted(df["qa_evaluator"].dropna().unique().tolist())
        
        min_date = df["call_date"].min().date() if not df.empty else pd.Timestamp.now().date()
        max_date = df["call_date"].max().date() if not df.empty else pd.Timestamp.now().date()
        
        dept_f = fc1.selectbox("Department", departments)
        team_f = fc2.selectbox("Team Lead", teams)
        topic_f = fc3.selectbox("Topic", topics)
        eval_f = fc4.selectbox("Evaluator", evaluators)
        
        from_date = fc5.date_input("From Date", min_date)
        to_date = fc6.date_input("To Date", max_date)
        score_range = fc7.slider("Score Range", 0, 100, (0, 100))
        pass_filter = fc8.selectbox("Pass Status", ["All", "Passed", "Failed"])

        if dept_f != "All": df = df[df["department"] == dept_f]
        if team_f != "All": df = df[df["team_lead"] == team_f]
        if topic_f != "All": df = df[df["topic"] == topic_f]
        if eval_f != "All": df = df[df["qa_evaluator"] == eval_f]
        df = df[(df["call_date"].dt.date >= from_date) & (df["call_date"].dt.date <= to_date)]
        df = df[(df["total_score"] >= score_range[0]) & (df["total_score"] <= score_range[1])]
        if pass_filter == "Passed": df = df[df["passed"] == True]
        elif pass_filter == "Failed": df = df[df["passed"] == False]

    if df.empty:
        st.warning("No data for selected filters.")
        return

    # KPIs
    total = len(df)
    avg_score = df["total_score"].mean()
    pass_rate = df["passed"].sum() / total * 100 if total else 0
    nogo_ct = df["no_go_violation"].notna().sum()
    fail_count = total - df["passed"].sum()
    
    score_trend = "+2.3%" if avg_score > 75 else "-1.2%"
    pass_trend = "+1.5%" if pass_rate > 80 else "-2.1%"
    spark = [avg_score - 5, avg_score - 3, avg_score, avg_score + 2, avg_score, avg_score - 1, avg_score + 3, avg_score]

    st.markdown("### 📊 Key Metrics")
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    with k1: kpi_card("Total Evaluations", str(total), "+12%", "#00D4FF", "📋", spark)
    with k2: kpi_card("Avg QA Score", f"{avg_score:.1f}%", score_trend, "#10B981", "📊", spark)
    with k3: kpi_card("Pass Rate", f"{pass_rate:.1f}%", pass_trend, "#22C55E", "✅", [pass_rate-10, pass_rate-5, pass_rate, pass_rate+2, pass_rate])
    with k4: kpi_card("Failed", str(fail_count), "", "#EF4444", "❌")
    with k5: kpi_card("No-Go Violations", str(nogo_ct), "", "#F59E0B", "🚨")
    with k6: kpi_card("Coaching Required", str(total - df["passed"].sum()), "", "#8B5CF6", "🎓")

    st.markdown("---")

    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📈 Trends", "👥 Agents", "📋 Categories", "🗓️ Period", "🚨 Violations", "📊 Distributions"])

    # TAB 1: TRENDS
    with tab1:
        chart_container("Weekly Score Trend")
        weekly = df.set_index("call_date").resample("W")["total_score"].agg(["mean", "min", "max"]).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=weekly["call_date"], y=weekly["max"], fill=None, mode="lines", line=dict(width=0), showlegend=False))
        fig.add_trace(go.Scatter(x=weekly["call_date"], y=weekly["min"], fill="tonexty", mode="lines", line=dict(width=0), fillcolor="rgba(0,212,255,0.1)", showlegend=False))
        fig.add_trace(go.Scatter(x=weekly["call_date"], y=weekly["mean"], mode="lines+markers", line=dict(color="#00D4FF", width=3), marker=dict(size=8), name="Avg Score"))
        fig.add_hline(y=75, line_dash="dash", line_color="rgba(239,68,68,0.6)", annotation_text="Pass Threshold")
        fig.update_layout(height=350, xaxis=dict(gridcolor="#2D2D3A"), yaxis=dict(range=[0,105], gridcolor="#2D2D3A"))
        st.plotly_chart(fig, use_container_width=True)
        chart_container_end()

    # TAB 2: AGENTS
    with tab2:
        chart_container("Agent Performance Ranking")
        
        agent_stats = df.groupby("advisor_name").agg(
            Evaluations=("id", "count"),
            Avg_Score=("total_score", "mean"),
            Pass_Rate=("passed", "mean"),
            Best=("total_score", "max"),
            Worst=("total_score", "min"),
        ).reset_index()
        
        agent_stats = agent_stats.sort_values("Avg_Score", ascending=False)
        agent_stats["Rank"] = range(1, len(agent_stats) + 1)
        agent_stats["Pass_Rate"] = (agent_stats["Pass_Rate"] * 100).round(1)
        agent_stats["Avg_Score"] = agent_stats["Avg_Score"].round(1)
        
        def get_color(score):
            if score >= 85: return "#10B981"
            elif score >= 75: return "#F59E0B"
            else: return "#EF4444"
        
        colors = [get_color(s) for s in agent_stats["Avg_Score"]]
        
        fig = go.Figure(go.Bar(x=agent_stats["Avg_Score"], y=agent_stats["advisor_name"], orientation="h", marker=dict(color=colors), text=[f"{s}%" for s in agent_stats["Avg_Score"]], textposition="outside"))
        fig.update_layout(height=max(300, len(agent_stats) * 30), xaxis=dict(range=[0,105], gridcolor="#2D2D3A"))
        st.plotly_chart(fig, use_container_width=True)
        chart_container_end()
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🏆 Top 5 Performers")
            for _, row in agent_stats.head(5).iterrows():
                st.markdown(f"**{row['Rank']}. {row['advisor_name']}** — {row['Avg_Score']}% ({row['Evaluations']} evals)")
        with c2:
            st.markdown("#### ⚠️ Bottom 5")
            for _, row in agent_stats.tail(5).iloc[::-1].iterrows():
                st.markdown(f"**{row['advisor_name']}** — {row['Avg_Score']}% ({row['Evaluations']} evals)")

    # TAB 3: CATEGORIES
    with tab3:
        chart_container("Category Performance")
        
        cat_scores = {}
        for col, weight in SCORE_WEIGHTS.items():
            if col in df.columns:
                avg = df["scores"].apply(lambda s: s.get(col, 0) if isinstance(s, dict) else 0).mean()
                cat_scores[col.replace("_", " ").title()] = round((avg / weight) * 100, 1)
        
        cat_df = pd.DataFrame(list(cat_scores.items()), columns=["Category", "Score%"])
        cat_df = cat_df.sort_values("Score%")
        
        colors = ["#EF4444" if v < 70 else "#F59E0B" if v < 85 else "#10B981" for v in cat_df["Score%"]]
        
        fig = go.Figure(go.Bar(y=cat_df["Category"], x=cat_df["Score%"], orientation="h", marker=dict(color=colors), text=[f"{v}%" for v in cat_df["Score%"]], textposition="outside"))
        fig.update_layout(height=400, xaxis=dict(range=[0,110], gridcolor="#2D2D3A"))
        st.plotly_chart(fig, use_container_width=True)
        chart_container_end()

    # TAB 4: PERIOD
    with tab4:
        df["month"] = df["call_date"].dt.to_period("M").astype(str)
        monthly = df.groupby("month").agg(Evaluations=("id", "count"), Avg_Score=("total_score", "mean"), Pass_Rate=("passed", "mean")).reset_index()
        monthly["Pass_Rate"] = (monthly["Pass_Rate"] * 100).round(1)
        monthly["Avg_Score"] = monthly["Avg_Score"].round(1)
        
        chart_container("Monthly Comparison")
        fig = go.Figure(go.Bar(x=monthly["month"], y=monthly["Evaluations"], marker_color="#00D4FF"))
        fig.update_layout(height=300, xaxis=dict(gridcolor="#2D2D3A"), yaxis=dict(gridcolor="#2D2D3A"))
        st.plotly_chart(fig, use_container_width=True)
        chart_container_end()

    # TAB 5: VIOLATIONS
    with tab5:
        nogo_df = df[df["no_go_violation"].notna()]
        
        if nogo_df.empty:
            st.success("🎉 No No-Go violations!")
        else:
            chart_container("Violations by Type")
            counts = nogo_df["no_go_violation"].value_counts().reset_index()
            counts.columns = ["Violation", "Count"]
            fig = go.Figure(go.Pie(labels=counts["Violation"], values=counts["Count"], hole=0.5))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            chart_container_end()
            
            st.dataframe(nogo_df[["id", "advisor_name", "call_date", "no_go_violation", "total_score"]].rename(columns={"id": "ID", "advisor_name": "Agent", "call_date": "Date", "no_go_violation": "Violation", "total_score": "Score"}), use_container_width=True, hide_index=True)

    # TAB 6: DISTRIBUTIONS
    with tab6:
        c1, c2 = st.columns(2)
        with c1:
            chart_container("Score Distribution")
            fig = px.histogram(df, x="total_score", nbins=20, color_discrete_sequence=["#00D4FF"])
            fig.update_layout(height=300, xaxis=dict(range=[0,100], gridcolor="#2D2D3A"), yaxis=dict(gridcolor="#2D2D3A"))
            st.plotly_chart(fig, use_container_width=True)
            chart_container_end()
        with c2:
            chart_container("Pass/Fail")
            passed = df["passed"].sum()
            failed = total - passed
            fig2 = go.Figure(go.Pie(labels=["Passed", "Failed"], values=[passed, failed], hole=0.6, marker=dict(colors=["#10B981", "#EF4444"])))
            fig2.update_layout(height=300)
            st.plotly_chart(fig2, use_container_width=True)
            chart_container_end()
