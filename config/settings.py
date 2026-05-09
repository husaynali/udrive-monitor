"""
Application Configuration & Constants
UDrive Quality Monitoring Platform
"""

APP_CONFIG = {
    "name": "UDrive Monitor",
    "version": "2.0.0",
    "company": "U-Drive",
    "qa_pass_threshold": 75,
    "coaching_required_threshold": 70,
    "high_risk_threshold": 60,
}

ROLES = {
    "super_admin": {"label": "Super Admin", "color": "#00D4FF", "pages": "all"},
    "qa_admin": {"label": "QA Admin", "color": "#8B5CF6", "pages": ["dashboard_*", "evaluation_*", "evaluations_*", "reports", "admin_*", "audit_logs"]},
    "qa_evaluator": {"label": "QA Evaluator", "color": "#10B981", "pages": ["dashboard_executive", "dashboard_qa", "evaluation_form", "evaluations_list", "reports"]},
    "team_leader": {"label": "Team Leader", "color": "#F59E0B", "pages": ["dashboard_executive", "dashboard_qa", "dashboard_coaching", "dashboard_agent", "evaluations_list", "coaching_form", "coaching_list", "reports"]},
    "coach": {"label": "Coach", "color": "#06B6D4", "pages": ["coaching_form", "coaching_list", "dashboard_coaching", "reports"]},
    "ops_manager": {"label": "Operations Manager", "color": "#EC4899", "pages": ["dashboard_*", "evaluations_list", "coaching_list", "reports"]},
    "agent": {"label": "Agent", "color": "#64748B", "pages": ["dashboard_agent"]},
    "viewer": {"label": "Read-Only Viewer", "color": "#94A3B8", "pages": ["dashboard_*", "reports"]},
}

# UDrive-specific departments (ride-sharing platform)
DEPARTMENTS = [
    "Driver Operations", "Rider Support", "Technical Support", 
    "Billing & Payments", "Safety & Compliance", "Sales", 
    "Operations", "Back Office", "Customer Experience",
]

# UDrive-specific audit types
AUDIT_TYPES = [
    "Live Monitoring", "Call Recording", "Chat Audit", 
    "Email Audit", "Screen Recording", "In-App Support", 
    "Emergency Calls", "Mystery Shopper",
]

# UDrive-specific topics
TOPICS = {
    "Driver Support": ["Registration", "Verification", "Driver Documents", "Vehicle Issues", "Earnings", "Trips", "Rating Appeals", "Driver Safety"],
    "Rider Support": ["Ride Issues", "Cancellation", "Refund Requests", "Payment Problems", "Safety Concerns", "Lost Items", "Accessibility"],
    "Technical Support": ["App Issues", "Login Problems", "Payment Failures", "Map/GPS Issues", "Notification Problems", "Device Compatibility"],
    "Safety & Compliance": ["Emergency Response", "Incident Reports", "Policy Violations", "Background Checks", "Driver Background", "Rider Safety"],
    "Billing & Payments": ["Charge Disputes", "Refund Requests", "Payment Methods", "Invoice Queries", "Promo Codes", "Fare Disputes"],
    "Sales & Partnerships": ["New Driver Signup", "Corporate Accounts", "Partnership Inquiries", "Promotions", "Referral Programs"],
    "General Inquiry": ["App Features", "Policy Questions", "Feedback", "Other"],
}

COACHING_TYPES = [
    "Performance Improvement", "Skill Development", "Compliance Remediation",
    "Behavioural Coaching", "Role Play", "Knowledge Gap", "Follow-Up",
    "Safety Training", "Customer Service Excellence", "De-escalation",
]

COACHING_STATUS = [
    "Scheduled", "In Progress", "Completed", "Cancelled", "Pending Agent",
]

# UDrive-specific skills/queues
SKILLS_QUEUES = [
    "General Support", "Priority Support", "Driver Queue", "Rider Queue",
    "Technical Support", "Billing Queue", "Escalations", "Safety & Emergency",
    "Sales Queue", "Retention Queue", "Live Chat", "Phone Support",
]

# UDrive-specific root causes
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
    "Safety protocol violation",
    "Customer handling",
]

TRAINING_MODULES = [
    "Communication Excellence", "Verification Protocols", "De-escalation Techniques",
    "Product Knowledge Refresh", "CRM System Training", "Compliance & Safety",
    "Call Handling Best Practices", "Documentation Standards", "SOP Refresher",
    "Emergency Response", "Customer Empathy", "Conflict Resolution",
]

# UDrive-specific No-Go violations
NO_GO_VIOLATIONS = [
    "Verification Failure",
    "Safety Protocol Violation",
    "Call Avoidance",
    "Unreasonable Deflection",
    "Confidentiality Breach",
    "Misbehavior / Unprofessional Conduct",
    "Emergency Handling Failure",
    "Regulatory Compliance Breach",
]

# UDrive quality score weights
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
