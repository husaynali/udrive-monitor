"""
Reports & Export Center
Redesigned with U-Drive Enterprise UI
"""

import streamlit as st
import pandas as pd
import io
from datetime import date
from utils.theme import section_header, chart_container, chart_container_end


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

            # KPI metrics
            from utils.theme import kpi_card
            m_cols = st.columns(4)
            with m_cols[0]:
                kpi_card("Total Evaluations", str(total), "", "#7C3AED", "📋")
            with m_cols[1]:
                kpi_card("Avg QA Score", f"{avg:.1f}%", "", "#10B981", "📊")
            with m_cols[2]:
                kpi_card("Pass Rate", f"{pr:.1f}%", "", "#22C55E", "✅")
            with m_cols[3]:
                kpi_card("No-Go Count", str(nogo), "", "#EF4444", "🚨")

            st.markdown("---")

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
                display = filtered[[
                    "id","advisor_name","call_date","topic","total_score","passed","no_go_violation","qa_evaluator"
                ]].copy()
                display.columns = ["ID","Agent","Date","Topic","Score","Passed","No-Go","Evaluator"]
                display["Score"]  = display["Score"].apply(lambda x: f"{x:.0f}%")
                display["Passed"] = display["Passed"].apply(lambda x: "PASS" if x else "FAIL")
                display["No-Go"]  = display["No-Go"].fillna("—")
                display["Date"]   = display["Date"].dt.strftime("%Y-%m-%d")
                st.dataframe(display, use_container_width=True, hide_index=True)

            # Export - Fixed: Proper tabular format
            st.markdown("### Export Data")
            
            export_col1, export_col2 = st.columns(2)
            
            # CSV Export with proper formatting
            export_df = filtered.drop(columns=["scores"], errors="ignore").copy()
            # Clean up the data for export
            export_df["call_date"] = export_df["call_date"].dt.strftime("%Y-%m-%d")
            export_df["total_score"] = export_df["total_score"].round(2)
            export_df["passed"] = export_df["passed"].map({True: "PASS", False: "FAIL"})
            export_df["no_go_violation"] = export_df["no_go_violation"].fillna("")
            
            csv_data = export_df.to_csv(index=False).encode("utf-8-sig")  # Add BOM for Excel UTF-8
            
            with export_col1:
                st.download_button(
                    "⬇️ Download CSV",
                    csv_data,
                    f"qa_report_{date.today()}.csv",
                    "text/csv;charset=utf-8-sig",
                    use_container_width=True
                )

            # Excel Export with proper formatting
            with export_col2:
                excel_buf = io.BytesIO()
                with pd.ExcelWriter(excel_buf, engine="openpyxl") as writer:
                    # Write the dataframe to Excel
                    export_df.to_excel(writer, sheet_name="QA Report", index=False, startrow=0)
                    
                    # Get the workbook to format headers
                    workbook = writer.book
                    worksheet = writer.sheets["QA Report"]
                    
                    # Format header row
                    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
                    
                    header_font = Font(bold=True, color="FFFFFF")
                    header_fill = PatternFill(start_color="7C3AED", end_color="7C3AED", fill_type="solid")
                    header_alignment = Alignment(horizontal="center", vertical="center")
                    thin_border = Border(
                        left=Side(style='thin'),
                        right=Side(style='thin'),
                        top=Side(style='thin'),
                        bottom=Side(style='thin')
                    )
                    
                    # Apply header formatting
                    for cell in worksheet[1]:
                        cell.font = header_font
                        cell.fill = header_fill
                        cell.alignment = header_alignment
                        cell.border = thin_border
                    
                    # Auto-fit column widths
                    for column in worksheet.columns:
                        max_length = 0
                        column_letter = column[0].column_letter
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        adjusted_width = min(max_length + 2, 50)
                        worksheet.column_dimensions[column_letter].width = adjusted_width
                
                excel_data = excel_buf.getvalue()
                st.download_button(
                    "⬇️ Download Excel",
                    excel_data,
                    f"qa_report_{date.today()}.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
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

            coach_cols = st.columns(3)
            with coach_cols[0]:
                kpi_card("Total Sessions", str(total_s), "", "#7C3AED", "🎓")
            with coach_cols[1]:
                kpi_card("Completed", str(comp_s), "", "#10B981", "✅")
            with coach_cols[2]:
                kpi_card("Completion Rate", f"{rate_s:.1f}%", "", "#22C55E", "📊")

            st.markdown("---")

            display_s = sdf[[
                "id","advisor_name","coaching_date","coaching_type","completion_status","qa_score","coach_name"
            ]].copy()
            display_s.columns = ["ID","Agent","Date","Type","Status","QA Score","Coach"]
            display_s["QA Score"] = display_s["QA Score"].apply(lambda x: f"{float(x):.0f}%" if pd.notna(x) else "—")
            display_s["Date"] = pd.to_datetime(display_s["Date"]).dt.strftime("%Y-%m-%d")
            st.dataframe(display_s, use_container_width=True, hide_index=True)

            # Export CSV
            export_s = sdf.copy()
            export_s["coaching_date"] = pd.to_datetime(export_s["coaching_date"]).dt.strftime("%Y-%m-%d")
            export_s["qa_score"] = export_s["qa_score"].apply(lambda x: f"{x:.1f}" if pd.notna(x) else "")
            
            csv_s = export_s.to_csv(index=False).encode("utf-8-sig")
            st.download_button("⬇️ Download CSV", csv_s, f"coaching_report_{date.today()}.csv", "text/csv;charset=utf-8-sig")

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

            export_p = perf.copy()
            export_p["Avg_Score"] = export_p["Avg_Score"].str.replace("%", "").astype(float)
            csv_p = export_p.to_csv(index=False).encode("utf-8-sig")
            st.download_button("⬇️ Download CSV", csv_p, f"agent_performance_{date.today()}.csv", "text/csv;charset=utf-8-sig")

    # ── Compliance Report ──────────────────────────────────────────────────
    with tabs[3]:
        st.markdown("### Compliance & No-Go Violations Report")
        if not evals:
            st.info("No data.")
        else:
            df3 = pd.DataFrame(evals)
            nogo_df = df3[df3["no_go_violation"].notna()][[
                "id","advisor_name","call_date","no_go_violation","team_lead","qa_evaluator"
            ]].copy()
            nogo_df.columns = ["Eval ID","Agent","Date","Violation","Team Lead","Evaluator"]
            nogo_df["Date"] = pd.to_datetime(nogo_df["Date"]).dt.strftime("%Y-%m-%d")

            if nogo_df.empty:
                st.success("🎉 No No-Go violations in the system!")
            else:
                st.error(f"⚠️ {len(nogo_df)} No-Go violation(s) on record")
                st.dataframe(nogo_df, use_container_width=True, hide_index=True)
                
                export_c = nogo_df.copy()
                csv_c = export_c.to_csv(index=False).encode("utf-8-sig")
                st.download_button("⬇️ Download CSV", csv_c, f"compliance_report_{date.today()}.csv", "text/csv;charset=utf-8-sig")
