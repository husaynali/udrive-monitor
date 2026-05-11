"""
Reports & Export Center
"""

import streamlit as st
import pandas as pd
import io
import json
from datetime import date
from utils.theme import section_header


def render():
    section_header("Reports & Export", "Generate and download operational reports in multiple formats")

    from utils.auth import load_evaluations, load_coaching_sessions
    evals = load_evaluations()
    sessions = load_coaching_sessions()

    tabs = st.tabs(["📋 QA Report", "🎓 Coaching Report", "👤 Agent Performance", "🔒 Compliance Report"])

    # ── QA Report ─────────────────────────────────────────────────────────
    with tabs[0]:
        st.markdown("### QA Evaluations Report")
        if not evals:
            st.info("No evaluations available.")
        else:
            df = pd.DataFrame(evals)
            df["call_date"] = pd.to_datetime(df["call_date"])

            # Config
            c1, c2, c3 = st.columns(3)
            from_d = c1.date_input("From", value=df["call_date"].min().date(), key="qa_from")
            to_d   = c2.date_input("To",   value=df["call_date"].max().date(), key="qa_to")
            group_by = c3.selectbox("Group By", ["Individual", "Team", "Department", "Topic"])

            mask = (df["call_date"].dt.date >= from_d) & (df["call_date"].dt.date <= to_d)
            filtered = df[mask]

            # Summary stats
            total = len(filtered)
            avg   = filtered["total_score"].mean() if total else 0
            pr    = filtered["passed"].sum() / total * 100 if total else 0
            nogo  = filtered["no_go_violation"].notna().sum()

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Evaluations", total)
            m2.metric("Avg QA Score",      f"{avg:.1f}%")
            m3.metric("Pass Rate",         f"{pr:.1f}%")
            m4.metric("No-Go Count",       nogo)

            if group_by == "Team":
                summary = filtered.groupby("team_lead").agg(
                    Evaluations=("id","count"),
                    Avg_Score=("total_score","mean"),
                    Pass_Count=("passed","sum"),
                ).reset_index()
                summary["Pass_Rate%"] = (summary["Pass_Count"] / summary["Evaluations"] * 100).round(1)
                st.dataframe(summary, use_container_width=True, hide_index=True)
            elif group_by == "Department":
                summary = filtered.groupby("department").agg(
                    Evaluations=("id","count"),
                    Avg_Score=("total_score","mean"),
                ).reset_index()
                st.dataframe(summary, use_container_width=True, hide_index=True)
            elif group_by == "Topic":
                summary = filtered.groupby("topic").agg(
                    Evaluations=("id","count"),
                    Avg_Score=("total_score","mean"),
                ).reset_index()
                st.dataframe(summary, use_container_width=True, hide_index=True)
            else:
                # Show key columns but export has ALL data
                display_cols = ["id","advisor_name","call_date","topic","total_score","passed","no_go_violation","qa_evaluator","monitoring_date"]
                display = filtered[display_cols].copy()
                display["Score"]  = display["total_score"].apply(lambda x: f"{x:.0f}")
                display["Pass"] = display["passed"].apply(lambda x: "PASS" if x else "FAIL")
                display["No-Go"]  = display["no_go_violation"].fillna("—")
                display["Date"]   = display["call_date"].dt.strftime("%Y-%m-%d")
                display["Mon Date"] = display["monitoring_date"].dt.strftime("%Y-%m-%d") if "monitoring_date" in display.columns else "—"
                st.dataframe(display[["id","advisor_name","Date","Mon Date","topic","Score","Pass","No-Go","qa_evaluator"]], use_container_width=True, hide_index=True)

            # Export ALL raw data from database - expand scores_json into separate columns
            col_dl1, col_dl2 = st.columns(2)
            
            # Get all columns from filtered data
            export_df = filtered.copy()
            
            # Expand scores_json (JSON) into separate columns
            if "scores_json" in export_df.columns:
                # Parse JSON and expand into separate columns
                scores_expanded = export_df["scores_json"].apply(
                    lambda x: json.loads(x) if isinstance(x, str) and x.startswith("{") else {}
                ).apply(pd.Series)
                # Rename columns with prefix
                scores_expanded.columns = [f"pillar_{c}" for c in scores_expanded.columns]
                # Merge with main dataframe
                export_df = pd.concat([export_df.drop(columns=["scores_json"]), scores_expanded], axis=1)
            
            # Format date columns
            date_cols = ["call_date", "monitoring_date", "created_at"]
            for dc in date_cols:
                if dc in export_df.columns:
                    try:
                        export_df[dc] = pd.to_datetime(export_df[dc]).dt.strftime("%Y-%m-%d %H:%M")
                    except:
                        pass
            
            # CSV export
            csv_data = export_df.to_csv(index=False).encode("utf-8")
            col_dl1.download_button("⬇️ Download CSV", csv_data, f"qa_report_{date.today()}.csv", "text/csv")

            # Excel export
            excel_buf = io.BytesIO()
            with pd.ExcelWriter(excel_buf, engine="openpyxl") as writer:
                export_df.to_excel(writer, sheet_name="QA Report", index=False)
            col_dl2.download_button(
                "⬇️ Download Excel",
                data=excel_buf.getvalue(),
                file_name=f"qa_report_{date.today()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

    # ── Coaching Report ────────────────────────────────────────────────────
    with tabs[1]:
        st.markdown("### Coaching Sessions Report")
        if not sessions:
            st.info("No coaching sessions available.")
        else:
            sdf = pd.DataFrame(sessions)
            total_s = len(sdf)
            comp_s  = (sdf["completion_status"] == "Completed").sum()
            rate_s  = comp_s / total_s * 100 if total_s else 0

            m1, m2, m3 = st.columns(3)
            m1.metric("Total Sessions", total_s)
            m2.metric("Completed",      comp_s)
            m3.metric("Completion Rate",f"{rate_s:.1f}%")

            display_s = sdf.copy()
            # Format dates for display (check if datetime first)
            if "coaching_date" in display_s.columns:
                try:
                    display_s["coaching_date"] = pd.to_datetime(display_s["coaching_date"]).dt.strftime("%Y-%m-%d")
                except:
                    pass
            st.dataframe(display_s, use_container_width=True, hide_index=True)

            # Export ALL raw data - include all columns
            csv_s = sdf.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download CSV", csv_s, f"coaching_report_{date.today()}.csv", "text/csv")

    # ── Agent Performance Report ───────────────────────────────────────────
    with tabs[2]:
        st.markdown("### Agent Performance Report")
        if not evals:
            st.info("No evaluations available.")
        else:
            df2 = pd.DataFrame(evals)
            perf = df2.groupby("advisor_name").agg(
                Evaluations=("id","count"),
                Avg_Score=("total_score","mean"),
                Pass_Count=("passed","sum"),
                NoGo_Count=("no_go_violation", lambda x: x.notna().sum()),
                Team=("team_lead","first"),
            ).reset_index()
            perf["Pass_Rate%"] = (perf["Pass_Count"] / perf["Evaluations"] * 100).round(1)
            perf["Risk"] = perf["Avg_Score"].apply(
                lambda s: "🟢 Low" if s >= 85 else "🟡 Medium" if s >= 75 else "🔴 High"
            )
            perf = perf.sort_values("Avg_Score", ascending=False)
            perf["Avg_Score"] = perf["Avg_Score"].apply(lambda x: f"{x:.1f}%")
            st.dataframe(perf, use_container_width=True, hide_index=True)

            csv_p = perf.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download CSV", csv_p, f"agent_performance_{date.today()}.csv", "text/csv")

    # ── Compliance Report ──────────────────────────────────────────────────
    with tabs[3]:
        st.markdown("### Compliance & No-Go Violations Report")
        if not evals:
            st.info("No data.")
        else:
            df3 = pd.DataFrame(evals)
            nogo_df = df3[df3["no_go_violation"].notna()].copy()

            if nogo_df.empty:
                st.success("🎉 No No-Go violations in the system!")
            else:
                st.error(f"⚠️ {len(nogo_df)} No-Go violation(s) on record")
                st.dataframe(nogo_df, use_container_width=True, hide_index=True)
                # Export ALL raw data (all columns from database)
                st.download_button("⬇️ Download CSV", csv_c, f"compliance_report_{date.today()}.csv", "text/csv")

