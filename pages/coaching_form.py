"""
New Coaching Session Form — Production (SQLite-backed)
"""

import streamlit as st
import uuid
from datetime import date, timedelta
from utils.theme import section_header
from utils.auth import current_user, log_action, load_failed_unlinked
from utils.database import save_coaching_session, mark_eval_coaching_linked
from config.settings import (
    COACHING_TYPES, COACHING_STATUS, DEPARTMENTS,
    ROOT_CAUSES, TRAINING_MODULES,
)


def render():
    section_header("New Coaching Session", "Document a coaching session linked to a QA evaluation")

    failed_evals = load_failed_unlinked()
    user         = current_user()

    eval_options = {f"{e['id']} — {e['advisor_name']} ({e['total_score']:.0f}%)": e for e in failed_evals}
    eval_options["Manual Entry (no linked evaluation)"] = None

    with st.form("coaching_form", clear_on_submit=True):

        st.markdown("### 🔵 A — Coaching Session Information")
        c1, c2, c3 = st.columns(3)
        linked_key = c1.selectbox("Linked QA Evaluation", list(eval_options.keys()))
        coach_type = c2.selectbox("Coaching Type", COACHING_TYPES)
        coach_date = c3.date_input("Coaching Date", value=date.today())
        linked_eval = eval_options[linked_key]

        st.markdown("---")
        st.markdown("### 🟡 B — People Information")
        c4, c5, c6 = st.columns(3)
        if linked_eval:
            advisor = c4.text_input("Advisor Name", value=linked_eval["advisor_name"], disabled=True)
            team_ld = c5.text_input("Team Lead",    value=linked_eval["team_lead"],    disabled=True)
            dept    = c6.text_input("Department",   value=linked_eval["department"],   disabled=True)
        else:
            advisor = c4.text_input("Advisor Name", placeholder="Agent full name")
            team_ld = c5.text_input("Team Lead",    placeholder="Team leader name")
            dept    = c6.selectbox("Department", DEPARTMENTS)
        coach_name = st.text_input("Coach Name", value=user.get("name",""), disabled=True)

        st.markdown("---")
        st.markdown("### 🟢 C — Evaluation Summary")
        if linked_eval:
            cs1, cs2, cs3, cs4 = st.columns(4)
            cs1.metric("QA Score",  f"{linked_eval['total_score']:.0f}%")
            cs2.metric("Result",    "PASS" if linked_eval["passed"] else "FAIL")
            cs3.metric("Topic",     linked_eval["topic"])
            cs4.metric("No-Go",     linked_eval.get("no_go_violation") or "None")
            linked_score  = linked_eval["total_score"]
            linked_result = "FAIL" if not linked_eval["passed"] else "PASS"
        else:
            cs1, cs2 = st.columns(2)
            linked_score  = cs1.number_input("QA Score (%)", 0, 100, 70)
            linked_result = cs2.selectbox("Result", ["FAIL","PASS"])

        st.markdown("---")
        st.markdown("### 🟠 D — Coaching Assessment Areas")
        st.markdown("**Communication Skills**")
        cc1, cc2, cc3, cc4 = st.columns(4)
        cc1.select_slider("Empathy",          ["Poor","Fair","Good","Excellent"])
        cc2.select_slider("Tone of Voice",    ["Poor","Fair","Good","Excellent"])
        cc3.select_slider("Active Listening", ["Poor","Fair","Good","Excellent"])
        cc4.select_slider("Professional Lang",["Poor","Fair","Good","Excellent"])

        st.markdown("**Operational Skills**")
        oc1, oc2, oc3, oc4 = st.columns(4)
        oc1.select_slider("Resolution Accuracy", ["Poor","Fair","Good","Excellent"])
        oc2.select_slider("Verification",        ["Poor","Fair","Good","Excellent"])
        oc3.select_slider("Documentation",       ["Poor","Fair","Good","Excellent"])
        oc4.select_slider("SOP Adherence",       ["Poor","Fair","Good","Excellent"])

        st.markdown("---")
        st.markdown("### 🟣 E — Strengths & Improvement Areas")
        ec1, ec2 = st.columns(2)
        strengths    = ec1.text_area("Strengths Identified",  height=110)
        improvements = ec2.text_area("Areas for Improvement", height=110)
        root_causes  = st.multiselect("Root Cause Analysis", ROOT_CAUSES)

        st.markdown("---")
        st.markdown("### 🔴 F — Corrective Action Plan")
        fc1, fc2 = st.columns(2)
        goals   = fc1.text_area("Improvement Goals", height=100)
        actions = fc2.text_area("Required Actions",  height=100)
        fc3, fc4, fc5 = st.columns(3)
        training    = fc3.selectbox("Assigned Training Module", TRAINING_MODULES)
        follow_up   = fc4.date_input("Follow-Up Date", value=date.today() + timedelta(days=14))
        comp_status = fc5.selectbox("Completion Status", COACHING_STATUS)

        st.markdown("---")
        st.markdown("### ✍️ G — Agent Acknowledgment")
        gc1, gc2 = st.columns(2)
        agent_feedback = gc1.text_area("Agent Feedback / Response",    height=100)
        commitment     = gc2.text_area("Agent Commitment Statement",   height=100)
        acknowledged   = st.checkbox("Agent has acknowledged this coaching session")

        st.markdown("---")
        submitted = st.form_submit_button("💾 Save Coaching Session", use_container_width=True)

    if submitted:
        cid = save_coaching_session({
            "related_eval_id":  linked_eval["id"] if linked_eval else None,
            "coaching_date":    str(coach_date),
            "coaching_type":    coach_type,
            "status":           comp_status,
            "advisor_name":     advisor,
            "agent_id":         linked_eval["agent_id"] if linked_eval else "—",
            "team_lead":        team_ld,
            "coach_name":       coach_name,
            "department":       linked_eval["department"] if linked_eval else dept,
            "qa_score":         linked_score,
            "result":           linked_result,
            "topic":            linked_eval["topic"] if linked_eval else "—",
            "no_go_violations": linked_eval.get("no_go_violation","None") if linked_eval else "None",
            "strengths":        strengths,
            "improvements":     improvements,
            "root_causes":      root_causes,
            "improvement_goals":goals,
            "actions_required": actions,
            "training_assigned":training,
            "follow_up_date":   str(follow_up),
            "completion_status":comp_status,
            "agent_feedback":   agent_feedback,
            "commitment":       commitment,
            "acknowledged":     acknowledged,
            "created_at":       str(date.today()),
            "created_by":       user.get("name",""),
        })

        if linked_eval:
            mark_eval_coaching_linked(linked_eval["id"])

        log_action("COACHING_CREATED", f"Coaching session {cid} for {advisor}")
        st.success(f"✅ Coaching session **{cid}** saved to database!")
