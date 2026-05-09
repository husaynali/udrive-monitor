"""
Application Configuration & Constants
"""

APP_CONFIG = {
    "name": "QA Pro Platform",
    "version": "2.0.0",
    "company": "U-Drive Design",
    "qa_pass_threshold": 75,
    "coaching_required_threshold": 70,
    "high_risk_threshold": 60,
}

ROLES = {
    "super_admin": {
        "label": "Super Admin",
        "color": "#FF4B6E",
        "pages": "all",
    },
    "qa_admin": {
        "label": "QA Admin",
        "color": "#F97316",
        "pages": ["dashboard_*", "evaluation_*", "evaluations_*", "reports", "admin_*", "audit_logs"],
    },
    "qa_evaluator": {
        "label": "QA Evaluator",
        "color": "#EAB308",
        "pages": ["dashboard_executive", "dashboard_qa", "evaluation_form", "evaluations_list", "reports"],
    },
    "team_leader": {
        "label": "Team Leader",
        "color": "#22C55E",
        "pages": ["dashboard_executive", "dashboard_qa", "dashboard_coaching", "dashboard_agent",
                  "evaluations_list", "coaching_form", "coaching_list", "reports"],
    },
    "coach": {
        "label": "Coach",
        "color": "#06B6D4",
        "pages": ["coaching_form", "coaching_list", "dashboard_coaching", "reports"],
    },
    "ops_manager": {
        "label": "Operations Manager",
        "color": "#8B5CF6",
        "pages": ["dashboard_*", "evaluations_list", "coaching_list", "reports"],
    },
    "agent": {
        "label": "Agent",
        "color": "#64748B",
        "pages": ["dashboard_agent"],
    },
    "viewer": {
        "label": "Read-Only Viewer",
        "color": "#94A3B8",
        "pages": ["dashboard_*", "reports"],
    },
}

DEPARTMENTS = [
    "Customer Support", "Technical Support", "Billing & Payments",
    "Retention", "Sales", "Operations", "Back Office", "Compliance",
]

AUDIT_TYPES = [
    "Live Monitoring", "Call Recording", "Email Audit",
    "Chat Audit", "Screen Recording", "Mystery Shopper",
]

TOPICS = {
    "Account Management": ["Password Reset", "Profile Update", "Account Closure", "Verification Issues"],
    "Billing & Payments": ["Charge Dispute", "Refund Request", "Payment Methods", "Invoice Queries"],
    "Technical Support": ["App Issues", "Connectivity", "Device Setup", "Bug Reports"],
    "Service Requests": ["New Service", "Upgrade", "Downgrade", "Cancellation"],
    "Complaints": ["Service Complaint", "Agent Complaint", "Policy Dispute", "Escalations"],
    "General Inquiry": ["Product Info", "Policy Inquiry", "Feedback", "Other"],
}

COACHING_TYPES = [
    "Performance Improvement", "Skill Development", "Compliance Remediation",
    "Behavioural Coaching", "Role Play", "Knowledge Gap", "Follow-Up",
]

COACHING_STATUS = [
    "Scheduled", "In Progress", "Completed", "Cancelled", "Pending Agent",
]

SKILLS_QUEUES = [
    "General Queue", "VIP Queue", "Technical Queue", "Billing Queue",
    "Escalation Queue", "Retention Queue", "Sales Queue",
]

ROOT_CAUSES = [
    "Lack of product knowledge",
    "Process non-compliance",
    "Poor communication skills",
    "Stress / Workload",
    "Inadequate training",
    "System/Tool issues",
    "Policy misunderstanding",
    "Attitude / Motivation",
    "Time management",
    "Verification gaps",
]

TRAINING_MODULES = [
    "Communication Excellence", "Verification Protocols", "De-escalation Techniques",
    "Product Knowledge Refresh", "CRM System Training", "Compliance & GDPR",
    "Call Handling Best Practices", "Documentation Standards", "SOP Refresher",
]

NO_GO_VIOLATIONS = [
    "Verification Failure",
    "Callback Failure",
    "Call Avoidance",
    "Unreasonable Deflection",
    "Confidentiality Breach",
    "Misbehavior / Unprofessional Conduct",
]

SCORE_WEIGHTS = {
    "greeting_format": 5,
    "closing_format": 5,
    "empathy_reassurance": 10,
    "effective_questions": 10,
    "attentiveness": 5,
    "tone_of_voice": 5,
    "waiting_procedures": 10,
    "delay_opening": 5,
    "grammar_punctuation": 5,
    "accurate_resolution": 20,
    "relevant_information": 5,
    "business_instructions": 10,
    "documentation_accuracy": 5,
}
