"""
Admin — System Settings (Production / SQLite persisted)
"""

import streamlit as st
from utils.theme import section_header
from utils.auth import require_auth, current_user, log_action
from utils.database import get_all_settings, set_setting


def _s(settings, key, default):
    val = settings.get(key, default)
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def render():
    require_auth()
    section_header("System Settings", "Configure platform rules, thresholds, SLAs, and notifications")

    settings = get_all_settings()
    user     = current_user()

    tab1, tab2, tab3 = st.tabs(["⚙️ QA Thresholds", "🔔 Notifications", "🔒 Security"])

    with tab1:
        st.markdown("### QA & Coaching Thresholds")
        c1, c2 = st.columns(2)
        pass_thresh     = c1.number_input("QA Pass Threshold (%)",             0, 100, _s(settings,"qa_pass_threshold",75))
        coaching_thresh = c2.number_input("Coaching Required Below (%)",       0, 100, _s(settings,"coaching_required_threshold",70))
        high_risk       = c1.number_input("High-Risk Agent Threshold (%)",     0, 100, _s(settings,"high_risk_threshold",60))
        critical        = c2.number_input("Critical Performance Threshold (%)",0, 100, _s(settings,"critical_threshold",50))

        st.markdown("### SLA Rules")
        sla1, sla2 = st.columns(2)
        coaching_sla = sla1.number_input("Coaching must be completed within (days)", 1, 30, _s(settings,"coaching_sla_days",7))
        follow_up    = sla2.number_input("Follow-up session within (days)",           1, 60, _s(settings,"follow_up_days",14))

        if st.button("Save Threshold Settings"):
            for key, val in [
                ("qa_pass_threshold", pass_thresh),
                ("coaching_required_threshold", coaching_thresh),
                ("high_risk_threshold", high_risk),
                ("critical_threshold", critical),
                ("coaching_sla_days", coaching_sla),
                ("follow_up_days", follow_up),
            ]:
                set_setting(key, str(val), user.get("name","System"))
            log_action("SETTINGS_UPDATED", "QA threshold settings updated")
            st.success("✅ Threshold settings saved to database.")

    with tab2:
        st.markdown("### Notification Rules")
        n_nogo   = st.checkbox("Email notification on No-Go violation",    value=bool(int(settings.get("notify_nogo","1"))))
        n_overdue= st.checkbox("Email notification when coaching overdue", value=bool(int(settings.get("notify_coaching_overdue","1"))))
        n_weekly = st.checkbox("Weekly performance digest to managers",    value=bool(int(settings.get("notify_weekly_digest","1"))))
        n_daily  = st.checkbox("Daily QA summary to team leads",           value=bool(int(settings.get("notify_daily_summary","0"))))

        st.markdown("### Email Configuration")
        nc1, nc2 = st.columns(2)
        nc1.text_input("SMTP Server",  placeholder="smtp.company.com")
        nc2.number_input("SMTP Port",  value=587)
        nc1.text_input("Sender Email", placeholder="qa-system@company.com")
        nc2.text_input("Sender Name",  placeholder="QA Pro Platform")

        if st.button("Save Notification Settings"):
            for key, val in [
                ("notify_nogo", int(n_nogo)),
                ("notify_coaching_overdue", int(n_overdue)),
                ("notify_weekly_digest", int(n_weekly)),
                ("notify_daily_summary", int(n_daily)),
            ]:
                set_setting(key, str(val), user.get("name","System"))
            log_action("SETTINGS_UPDATED", "Notification settings updated")
            st.success("✅ Notification settings saved to database.")

    with tab3:
        st.markdown("### Security & Access")
        s_mfa     = st.checkbox("Require MFA for all users",         value=bool(int(settings.get("require_mfa","0"))))
        s_expiry  = st.checkbox("Enforce password expiry (90 days)", value=bool(int(settings.get("password_expiry","1"))))
        s_lock    = st.checkbox("Lock account after 5 failed logins",value=bool(int(settings.get("lock_after_failures","1"))))
        s_log     = st.checkbox("Log all user actions",              value=bool(int(settings.get("log_all_actions","1"))))

        st.markdown("### Data Retention")
        dr1, dr2 = st.columns(2)
        data_ret  = dr1.number_input("Keep evaluation records (months)", 1, 120, _s(settings,"data_retention_months",24))
        audit_ret = dr2.number_input("Keep audit logs (months)",         1, 120, _s(settings,"audit_log_retention_months",12))

        if st.button("Save Security Settings"):
            for key, val in [
                ("require_mfa", int(s_mfa)),
                ("password_expiry", int(s_expiry)),
                ("lock_after_failures", int(s_lock)),
                ("log_all_actions", int(s_log)),
                ("data_retention_months", data_ret),
                ("audit_log_retention_months", audit_ret),
            ]:
                set_setting(key, str(val), user.get("name","System"))
            log_action("SETTINGS_UPDATED", "Security settings updated")
            st.success("✅ Security settings saved to database.")
