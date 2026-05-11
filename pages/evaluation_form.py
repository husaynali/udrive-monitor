"""
QA Evaluation Form — Production (saves to SQLite)
"""

import streamlit as st
import uuid
from datetime import date
from utils.theme import section_header
from utils.auth import current_user, log_action
from utils.database import save_evaluation, get_agents
from config.settings import (
    AUDIT_TYPES, TOPICS, SKILLS_QUEUES, DEPARTMENTS,
    NO_GO_VIOLATIONS, SCORE_WEIGHTS,
)


def _get_agents():
    """Fetch agents from DB, fall back to demo list."""
    db_agents = get_agents()
    if db_agents:
        return db_agents
    return [
        {"name": "agt-test",    "agent_id": "AGT-089", "department": "Customer Support"},
    ]


TL_MAP = {
    "AGT-089": "tl-test",  "AGT-102": "Mark Stevens",
}


def _score_row(label, key, max_val, weight_pct):
    col_label, col_input, col_comment = st.columns([3, 1, 2])
    with col_label:
        st.markdown(
            f'<div style="padding:0.5rem 0;font-size:0.9rem;color:#E2E8F0;font-weight:500">'
            f'{label} <span style="color:#64748B;font-size:0.8rem;">({weight_pct}%)</span></div>',
            unsafe_allow_html=True,
        )
    with col_input:
        val = st.number_input(
            f"Score", 
            min_value=0, 
            max_value=max_val, 
            value=max_val, 
            key=key,
            label_visibility="collapsed"
        )
        # Show score indicator
        color = "#10B981" if val == max_val else "#F59E0B" if val > max_val//2 else "#EF4444" if val > 0 else "#6B7280"
        st.markdown(
            f'<div style="text-align:center;padding:0.25rem;color:{color};'
            f'font-size:0.85rem;font-weight:600">{val}/{max_val}</div>',
            unsafe_allow_html=True,
        )
    with col_comment:
        # Comment/reason field for each pillar
        comment = st.text_area(
            f"Comment for {label}", 
            placeholder=f"Reason for score...",
            key=f"{key}_comment",
            label_visibility="collapsed",
            height=60
        )
        # Store in session state for saving
        if f"pillar_comments" not in st.session_state:
            st.session_state.pillar_comments = {}
        if comment:
            st.session_state.pillar_comments[key] = comment
    return val


def render():
    section_header("New QA Evaluation", "Complete all sections to submit an evaluation")

    agents = _get_agents()
    user   = current_user()

    with st.form("qa_evaluation_form", clear_on_submit=True):

        st.markdown("### 🔵 A — Interaction Information")
        c1, c2, c3 = st.columns(3)
        call_id    = c1.text_input("Call / Interaction ID", placeholder="CALL-123456")
        audit_type = c2.selectbox("Audit Type", AUDIT_TYPES)
        call_date  = c3.date_input("Call Date", value=date.today())

        c4, c5, c6 = st.columns(3)
        mon_date   = c4.date_input("Monitoring Date", value=date.today())
        topic      = c5.selectbox("Topic", list(TOPICS.keys()))
        subtopic   = c6.selectbox("Sub Topic", TOPICS.get(topic, [""]))

        c7, c8, c9 = st.columns(3)
        skill_q    = c7.selectbox("Skill / Queue", SKILLS_QUEUES)
        aht        = c8.number_input("AHT (seconds)", min_value=0, value=300)
        hold_time  = c9.number_input("Hold Time (seconds)", min_value=0, value=0)

        st.markdown("---")
        st.markdown("### 🟡 B — Agent Information")
        agent_names = [a["name"] for a in agents]
        c1, c2 = st.columns(2)
        advisor_name   = c1.selectbox("Advisor Name", agent_names)
        evaluator_name = c2.text_input("QA Evaluator", value=user.get("name",""), disabled=True)

        selected = next((a for a in agents if a["name"] == advisor_name), agents[0])
        c3, c4, c5 = st.columns(3)
        c3.text_input("Agent ID",  value=selected.get("agent_id",""), disabled=True)
        tl_val = TL_MAP.get(selected.get("agent_id",""), "—")
        c4.text_input("Team Lead", value=tl_val, disabled=True)
        dept = c5.selectbox("Department", DEPARTMENTS,
                             index=DEPARTMENTS.index("Customer Support") if "Customer Support" in DEPARTMENTS else 0)

        st.markdown("---")
        st.markdown("### 🟢 C — Greeting & Closing")
        score_greeting = _score_row("Greeting Format", "greeting_format", 5, 5)
        score_closing  = _score_row("Closing Format",  "closing_format",  5, 5)
        st.checkbox("Offered Additional Assistance")

        st.markdown("---")
        st.markdown("### 🟠 D — Engagement & Interaction")
        score_empathy = _score_row("Empathy / Reassurance", "empathy_reassurance", 10, 10)
        score_eff_q   = _score_row("Effective Questions",   "effective_questions",  10, 10)
        score_attn    = _score_row("Attentiveness",          "attentiveness",          5,  5)
        score_tone    = _score_row("Tone of Voice",          "tone_of_voice",           5,  5)

        st.markdown("---")
        st.markdown("### 🔵 E — Call Handling & Hold Etiquette")
        score_wait  = _score_row("Waiting Procedures", "waiting_procedures", 10, 10)
        score_delay = _score_row("Delay Opening",       "delay_opening",       5,  5)

        st.markdown("---")
        st.markdown("### 🟣 F — Typing & Language")
        score_grammar = _score_row("Grammar & Punctuation", "grammar_punctuation", 5, 5)
        pro_language  = st.selectbox("Professional Language", ["Pass", "Fail — No-Go Triggered"])

        st.markdown("---")
        st.markdown("### 🟢 G — Resolution Quality")
        score_res     = _score_row("Accurate Resolution",          "accurate_resolution",  20, 20)
        score_rel_inf = _score_row("Relevant Information Provided","relevant_information",  5,  5)

        st.markdown("---")
        st.markdown("### 🔴 H — Compliance & Verification (Critical No-Go)")
        st.warning("⚠️ Any No-Go violation will trigger automatic audit failure and coaching requirement.")
        nogo_violations = st.multiselect("Select any No-Go violations observed:", NO_GO_VIOLATIONS)

        st.markdown("---")
        st.markdown("### 🟡 I — Business Instructions & Documentation")
        score_biz_inst = _score_row("Following Business Instructions", "business_instructions",  10, 10)
        score_doc      = _score_row("Documentation Accuracy",           "documentation_accuracy",  5,  5)

        st.markdown("---")
        st.markdown("### 📝 J — QA Feedback & Coaching Notes")
        fc1, fc2 = st.columns(2)
        qa_comments     = fc1.text_area("QA Comments",       height=100)
        what_went_wrong = fc2.text_area("What Went Wrong",   height=100)
        fc3, fc4 = st.columns(2)
        positive_fb = fc3.text_area("Positive Feedback", height=100)
        action_req  = fc4.text_area("Action Required",   height=100)

        st.markdown("---")
        submitted = st.form_submit_button("✅ Submit Evaluation", use_container_width=True)

    if submitted:
        # Get pillar comments from session state
        pillar_comments = st.session_state.get("pillar_comments", {})
        
        scores = {
            "greeting_format":        score_greeting,
            "closing_format":         score_closing,
            "empathy_reassurance":    score_empathy,
            "effective_questions":    score_eff_q,
            "attentiveness":          score_attn,
            "tone_of_voice":          score_tone,
            "waiting_procedures":     score_wait,
            "delay_opening":          score_delay,
            "grammar_punctuation":    score_grammar,
            "accurate_resolution":    score_res,
            "relevant_information":   score_rel_inf,
            "business_instructions":  score_biz_inst,
            "documentation_accuracy": score_doc,
        }
        
        # Include pillar comments in scores for storage
        scores_with_comments = {}
        for k, v in scores.items():
            scores_with_comments[k] = {
                "score": v,
                "comment": pillar_comments.get(k, "")
            }
        
        raw_total = sum(s["score"] for s in scores_with_comments.values())
        has_nogo  = bool(nogo_violations) or pro_language.startswith("Fail")
        final     = 0 if has_nogo else raw_total
        passed    = not has_nogo and raw_total >= 75

        eid = save_evaluation({
            "call_id":          call_id or f"CALL-{uuid.uuid4().int % 999999:06d}",
            "audit_type":       audit_type,
            "call_date":        str(call_date),
            "monitoring_date":  str(mon_date),
            "topic":            topic,
            "subtopic":         subtopic,
            "skill_queue":      skill_q,
            "aht":              int(aht),
            "hold_time":        int(hold_time),
            "advisor_name":     advisor_name,
            "agent_id":         selected.get("agent_id",""),
            "team_lead":        tl_val,
            "department":       dept,
            "qa_evaluator":     user.get("name",""),
            "week_number":      date.today().isocalendar()[1],
            "scores":           scores_with_comments,
            "total_score":      final,
            "passed":           passed,
            "no_go_violation":  nogo_violations[0] if nogo_violations else None,
            "coaching_required":not passed,
            "qa_comments":      qa_comments,
            "what_went_wrong":  what_went_wrong,
            "positive_feedback":positive_fb,
            "action_required":  action_req,
            "created_at":       str(date.today()),
            "created_by":       user.get("name",""),
        })

        log_action("EVALUATION_CREATED", f"Evaluation {eid} for {advisor_name} — score {final}%")

        if has_nogo:
            st.error(f"❌ AUDIT FAILED — No-Go violation(s): {', '.join(nogo_violations)}")
        elif passed:
            st.success(f"✅ PASSED — Score: {final}%")
            st.balloons()
        else:
            st.warning(f"⚠️ FAILED — Score: {final}% (Threshold: 75%)")

        st.info(f"Evaluation **{eid}** saved to database. {'Coaching session required.' if not passed else ''}")
        
        # Clear session state for next evaluation
        if "pillar_comments" in st.session_state:
            st.session_state.pillar_comments = {}
