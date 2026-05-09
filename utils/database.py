"""
Production Database Layer — SQLite with full schema for QA Platform
All data operations go through this module.
"""

import sqlite3
import hashlib
import uuid
import json
import os
from datetime import datetime, date, timedelta
from contextlib import contextmanager
from typing import Optional

# ── Path ────────────────────────────────────────────────────────────────────
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "qa_platform.db")


@contextmanager
def get_conn():
    """Yield a connection with WAL mode, row factory, and FK enforcement."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ── Schema ───────────────────────────────────────────────────────────────────

SCHEMA = """
-- Users
CREATE TABLE IF NOT EXISTS users (
    id            TEXT PRIMARY KEY,
    name          TEXT NOT NULL,
    email         TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role          TEXT NOT NULL DEFAULT 'agent',
    department    TEXT,
    agent_id      TEXT,
    avatar        TEXT,
    is_active     INTEGER NOT NULL DEFAULT 1,
    created_at    TEXT NOT NULL,
    last_login    TEXT
);

-- Evaluations
CREATE TABLE IF NOT EXISTS evaluations (
    id                  TEXT PRIMARY KEY,
    call_id             TEXT,
    audit_type          TEXT,
    call_date           TEXT NOT NULL,
    monitoring_date     TEXT,
    topic               TEXT,
    subtopic            TEXT,
    skill_queue         TEXT,
    aht                 INTEGER DEFAULT 0,
    hold_time           INTEGER DEFAULT 0,
    advisor_name        TEXT NOT NULL,
    agent_id            TEXT,
    team_lead           TEXT,
    department          TEXT,
    qa_evaluator        TEXT,
    week_number         INTEGER,
    scores_json         TEXT,
    total_score         REAL DEFAULT 0,
    passed              INTEGER DEFAULT 0,
    no_go_violation     TEXT,
    coaching_required   INTEGER DEFAULT 0,
    coaching_linked     INTEGER DEFAULT 0,
    qa_comments         TEXT,
    what_went_wrong     TEXT,
    positive_feedback   TEXT,
    action_required     TEXT,
    created_at          TEXT NOT NULL,
    created_by          TEXT
);

-- Coaching Sessions
CREATE TABLE IF NOT EXISTS coaching_sessions (
    id                  TEXT PRIMARY KEY,
    related_eval_id     TEXT,
    coaching_date       TEXT NOT NULL,
    coaching_type       TEXT,
    status              TEXT DEFAULT 'Scheduled',
    advisor_name        TEXT NOT NULL,
    agent_id            TEXT,
    team_lead           TEXT,
    coach_name          TEXT,
    department          TEXT,
    qa_score            REAL DEFAULT 0,
    result              TEXT,
    topic               TEXT,
    no_go_violations    TEXT,
    strengths           TEXT,
    improvements        TEXT,
    root_causes_json    TEXT,
    improvement_goals   TEXT,
    actions_required    TEXT,
    training_assigned   TEXT,
    follow_up_date      TEXT,
    completion_status   TEXT DEFAULT 'Pending Agent',
    agent_feedback      TEXT,
    commitment          TEXT,
    acknowledged        INTEGER DEFAULT 0,
    created_at          TEXT NOT NULL,
    created_by          TEXT,
    FOREIGN KEY (related_eval_id) REFERENCES evaluations(id)
);

-- Audit Logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id          TEXT PRIMARY KEY,
    timestamp   TEXT NOT NULL,
    user_name   TEXT,
    user_role   TEXT,
    action      TEXT NOT NULL,
    detail      TEXT,
    ip_address  TEXT,
    session_id  TEXT
);

-- System Settings
CREATE TABLE IF NOT EXISTS settings (
    key         TEXT PRIMARY KEY,
    value       TEXT NOT NULL,
    updated_at  TEXT,
    updated_by  TEXT
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_eval_advisor    ON evaluations(advisor_name);
CREATE INDEX IF NOT EXISTS idx_eval_date       ON evaluations(call_date);
CREATE INDEX IF NOT EXISTS idx_eval_passed     ON evaluations(passed);
CREATE INDEX IF NOT EXISTS idx_eval_team       ON evaluations(team_lead);
CREATE INDEX IF NOT EXISTS idx_coaching_eval   ON coaching_sessions(related_eval_id);
CREATE INDEX IF NOT EXISTS idx_coaching_advisor ON coaching_sessions(advisor_name);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_user      ON audit_logs(user_name);
"""


def init_db():
    """Create all tables and seed default data if empty."""
    with get_conn() as conn:
        conn.executescript(SCHEMA)

    _seed_default_users()
    _seed_default_settings()
    _seed_demo_evaluations_if_empty()


# ── Default seeds ────────────────────────────────────────────────────────────

def _seed_default_users():
    """Seed the 5 demo users if users table is empty."""
    with get_conn() as conn:
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if count > 0:
            return

        now = datetime.now().isoformat()
        demo = [
            ("admin@qa-pro.com",     "Admin@123",  "Sarah Mitchell", "super_admin", "Quality Assurance",    "ADM-001", "SM"),
            ("evaluator@qa-pro.com", "Eval@123",   "James Thornton", "qa_evaluator","Quality Assurance",    "QAE-012", "JT"),
            ("coach@qa-pro.com",     "Coach@123",  "Amira Hassan",   "coach",       "Learning & Development","COA-005", "AH"),
            ("agent@qa-pro.com",     "Agent@123",  "Leon Davis",     "agent",       "Customer Support",     "AGT-089", "LD"),
            ("manager@qa-pro.com",   "Mgr@123",    "Priya Sharma",   "ops_manager", "Operations",           "OPS-003", "PS"),
        ]
        for email, pw, name, role, dept, agent_id, avatar in demo:
            conn.execute(
                """INSERT INTO users (id, name, email, password_hash, role, department, agent_id, avatar, is_active, created_at)
                   VALUES (?,?,?,?,?,?,?,?,1,?)""",
                (str(uuid.uuid4()), name, email,
                 hashlib.sha256(pw.encode()).hexdigest(),
                 role, dept, agent_id, avatar, now)
            )


def _seed_default_settings():
    now = datetime.now().isoformat()
    defaults = {
        "qa_pass_threshold": "75",
        "coaching_required_threshold": "70",
        "high_risk_threshold": "60",
        "critical_threshold": "50",
        "coaching_sla_days": "7",
        "follow_up_days": "14",
        "notify_nogo": "1",
        "notify_coaching_overdue": "1",
        "notify_weekly_digest": "1",
        "notify_daily_summary": "0",
        "require_mfa": "0",
        "password_expiry": "1",
        "lock_after_failures": "1",
        "log_all_actions": "1",
        "data_retention_months": "24",
        "audit_log_retention_months": "12",
    }
    with get_conn() as conn:
        for key, val in defaults.items():
            conn.execute(
                "INSERT OR IGNORE INTO settings (key, value, updated_at) VALUES (?,?,?)",
                (key, val, now)
            )


def _seed_demo_evaluations_if_empty():
    """Seed 60 demo evaluations if the table is empty."""
    with get_conn() as conn:
        count = conn.execute("SELECT COUNT(*) FROM evaluations").fetchone()[0]
        if count > 0:
            return

    import random

    agents = [
        {"name": "Leon Davis",    "id": "AGT-089", "tl": "Mark Stevens",  "dept": "Customer Support"},
        {"name": "Clara Bennett", "id": "AGT-102", "tl": "Mark Stevens",  "dept": "Customer Support"},
        {"name": "Omar Khalil",   "id": "AGT-115", "tl": "Sarah O'Brien", "dept": "Customer Support"},
        {"name": "Julia Torres",  "id": "AGT-078", "tl": "Sarah O'Brien", "dept": "Customer Support"},
        {"name": "Kwame Asante",  "id": "AGT-133", "tl": "David Park",    "dept": "Technical Support"},
        {"name": "Mia Lindqvist", "id": "AGT-044", "tl": "David Park",    "dept": "Technical Support"},
    ]
    topics = {
        "Account Management": ["Password Reset", "Profile Update"],
        "Billing & Payments": ["Charge Dispute", "Refund Request"],
        "Technical Support":  ["App Issues", "Connectivity"],
    }
    today = date.today()
    evals_to_insert = []
    coaching_to_insert = []

    for i in range(60):
        agent  = random.choice(agents)
        topic  = random.choice(list(topics.keys()))
        subtopic = random.choice(topics[topic])
        call_date = today - timedelta(days=random.randint(0, 89))
        scores = {
            "greeting_format":       random.choice([0, 5]),
            "closing_format":        random.choice([0, 5]),
            "empathy_reassurance":   random.randint(0, 10),
            "effective_questions":   random.randint(5, 10),
            "attentiveness":         random.choice([0, 5]),
            "tone_of_voice":         random.choice([0, 5]),
            "waiting_procedures":    random.randint(5, 10),
            "delay_opening":         random.choice([0, 5]),
            "grammar_punctuation":   random.randint(3, 5),
            "accurate_resolution":   random.randint(10, 20),
            "relevant_information":  random.choice([0, 5]),
            "business_instructions": random.randint(5, 10),
            "documentation_accuracy":random.choice([0, 5]),
        }
        raw  = sum(scores.values())
        nogo = random.choice(["Verification Failure","Callback Failure"]) if random.random() < 0.12 else None
        final = 0 if nogo else raw
        passed = (not nogo) and raw >= 75
        eid = f"EVL-{1000+i}"
        evals_to_insert.append({
            "id": eid,
            "call_id": f"CALL-{random.randint(100000,999999)}",
            "audit_type": random.choice(["Live Monitoring","Call Recording"]),
            "call_date": call_date.isoformat(),
            "monitoring_date": today.isoformat(),
            "topic": topic,
            "subtopic": subtopic,
            "skill_queue": random.choice(["General Queue","Billing Queue","Technical Queue"]),
            "aht": random.randint(180, 720),
            "hold_time": random.randint(0, 120),
            "advisor_name": agent["name"],
            "agent_id": agent["id"],
            "team_lead": agent["tl"],
            "department": agent["dept"],
            "qa_evaluator": "James Thornton",
            "week_number": call_date.isocalendar()[1],
            "scores_json": json.dumps(scores),
            "total_score": final,
            "passed": 1 if passed else 0,
            "no_go_violation": nogo,
            "coaching_required": 0 if passed else 1,
            "coaching_linked": 0,
            "qa_comments": "Evaluation completed.",
            "what_went_wrong": "" if passed else "Performance below threshold.",
            "positive_feedback": "Good effort.",
            "action_required": "" if passed else "Review SOP and retrain.",
            "created_at": call_date.isoformat(),
            "created_by": "James Thornton",
        })

        if not passed:
            coaching_to_insert.append({
                "id": f"CSN-{2000+i}",
                "related_eval_id": eid,
                "coaching_date": call_date.isoformat(),
                "coaching_type": random.choice(["Performance Improvement","Compliance Remediation"]),
                "status": random.choice(["Completed","In Progress","Scheduled"]),
                "advisor_name": agent["name"],
                "agent_id": agent["id"],
                "team_lead": agent["tl"],
                "coach_name": "Amira Hassan",
                "department": agent["dept"],
                "qa_score": final,
                "result": "FAIL",
                "topic": topic,
                "no_go_violations": nogo or "None",
                "strengths": "Good communication tone.",
                "improvements": "Verification process must be followed.",
                "root_causes_json": json.dumps(["Process non-compliance"]),
                "improvement_goals": "Achieve 80%+ on next evaluation.",
                "actions_required": "Complete verification training module.",
                "training_assigned": "Verification Protocols",
                "follow_up_date": (today + timedelta(days=14)).isoformat(),
                "completion_status": random.choice(["Completed","In Progress","Pending Agent"]),
                "agent_feedback": "",
                "commitment": "",
                "acknowledged": 0,
                "created_at": call_date.isoformat(),
                "created_by": "Amira Hassan",
            })

    with get_conn() as conn:
        conn.executemany(
            """INSERT INTO evaluations
               (id,call_id,audit_type,call_date,monitoring_date,topic,subtopic,skill_queue,aht,hold_time,
                advisor_name,agent_id,team_lead,department,qa_evaluator,week_number,scores_json,total_score,
                passed,no_go_violation,coaching_required,coaching_linked,qa_comments,what_went_wrong,
                positive_feedback,action_required,created_at,created_by)
               VALUES (:id,:call_id,:audit_type,:call_date,:monitoring_date,:topic,:subtopic,:skill_queue,
                       :aht,:hold_time,:advisor_name,:agent_id,:team_lead,:department,:qa_evaluator,
                       :week_number,:scores_json,:total_score,:passed,:no_go_violation,:coaching_required,
                       :coaching_linked,:qa_comments,:what_went_wrong,:positive_feedback,:action_required,
                       :created_at,:created_by)""",
            evals_to_insert
        )
        conn.executemany(
            """INSERT INTO coaching_sessions
               (id,related_eval_id,coaching_date,coaching_type,status,advisor_name,agent_id,team_lead,
                coach_name,department,qa_score,result,topic,no_go_violations,strengths,improvements,
                root_causes_json,improvement_goals,actions_required,training_assigned,follow_up_date,
                completion_status,agent_feedback,commitment,acknowledged,created_at,created_by)
               VALUES (:id,:related_eval_id,:coaching_date,:coaching_type,:status,:advisor_name,:agent_id,
                       :team_lead,:coach_name,:department,:qa_score,:result,:topic,:no_go_violations,
                       :strengths,:improvements,:root_causes_json,:improvement_goals,:actions_required,
                       :training_assigned,:follow_up_date,:completion_status,:agent_feedback,:commitment,
                       :acknowledged,:created_at,:created_by)""",
            coaching_to_insert
        )


# ── Helper: Row → dict ────────────────────────────────────────────────────────

def _row(r):
    if r is None:
        return None
    d = dict(r)
    # Deserialise JSON blobs
    for k in ("scores_json", "root_causes_json"):
        if k in d and d[k]:
            d[k.replace("_json", "")] = json.loads(d[k])
    return d


def _rows(rs):
    return [_row(r) for r in rs]


# ══════════════════════════════════════════════════════════════════════════════
#  AUTH / USERS
# ══════════════════════════════════════════════════════════════════════════════

def authenticate_user(email: str, password: str):
    """Returns user dict on success, None on failure."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE email=? AND is_active=1",
            (email.lower().strip(),)
        ).fetchone()
    if not row:
        return None
    h = hashlib.sha256(password.encode()).hexdigest()
    if h != row["password_hash"]:
        return None
    # Update last_login
    with get_conn() as conn:
        conn.execute(
            "UPDATE users SET last_login=? WHERE id=?",
            (datetime.now().isoformat(), row["id"])
        )
    return _row(row)


def get_all_users():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM users ORDER BY name").fetchall()
    return _rows(rows)


def create_user(name, email, password, role, department, agent_id=""):
    uid = str(uuid.uuid4())
    avatar = "".join([w[0].upper() for w in name.split()[:2]])
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO users (id,name,email,password_hash,role,department,agent_id,avatar,is_active,created_at)
               VALUES (?,?,?,?,?,?,?,?,1,?)""",
            (uid, name, email.lower(),
             hashlib.sha256(password.encode()).hexdigest(),
             role, department, agent_id or f"USR-{uid[:4].upper()}", avatar,
             datetime.now().isoformat())
        )
    return uid


def update_user_role(user_name: str, new_role: str):
    with get_conn() as conn:
        conn.execute("UPDATE users SET role=? WHERE name=?", (new_role, user_name))


def deactivate_user(user_id: str):
    with get_conn() as conn:
        conn.execute("UPDATE users SET is_active=0 WHERE id=?", (user_id,))


def get_agents():
    """Return list of agent-role users for dropdowns."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT name, agent_id, department FROM users WHERE role='agent' AND is_active=1 ORDER BY name"
        ).fetchall()
    return _rows(rows)


# ══════════════════════════════════════════════════════════════════════════════
#  EVALUATIONS
# ══════════════════════════════════════════════════════════════════════════════

def save_evaluation(record: dict) -> str:
    eid = record.get("id") or f"EVL-{str(uuid.uuid4())[:6].upper()}"
    scores = record.get("scores", {})
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO evaluations
               (id,call_id,audit_type,call_date,monitoring_date,topic,subtopic,skill_queue,aht,hold_time,
                advisor_name,agent_id,team_lead,department,qa_evaluator,week_number,scores_json,total_score,
                passed,no_go_violation,coaching_required,coaching_linked,qa_comments,what_went_wrong,
                positive_feedback,action_required,created_at,created_by)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                eid,
                record.get("call_id",""),
                record.get("audit_type",""),
                str(record.get("call_date","")),
                str(record.get("monitoring_date","")),
                record.get("topic",""),
                record.get("subtopic",""),
                record.get("skill_queue",""),
                int(record.get("aht",0)),
                int(record.get("hold_time",0)),
                record.get("advisor_name",""),
                record.get("agent_id",""),
                record.get("team_lead",""),
                record.get("department",""),
                record.get("qa_evaluator",""),
                record.get("week_number",0),
                json.dumps(scores),
                float(record.get("total_score",0)),
                1 if record.get("passed") else 0,
                record.get("no_go_violation"),
                1 if record.get("coaching_required") else 0,
                0,
                record.get("qa_comments",""),
                record.get("what_went_wrong",""),
                record.get("positive_feedback",""),
                record.get("action_required",""),
                str(record.get("created_at", date.today())),
                record.get("created_by",""),
            )
        )
    return eid


def get_all_evaluations():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM evaluations ORDER BY call_date DESC").fetchall()
    result = []
    for r in rows:
        d = _row(r)
        d["passed"] = bool(d["passed"])
        d["coaching_required"] = bool(d["coaching_required"])
        d["coaching_linked"] = bool(d["coaching_linked"])
        result.append(d)
    return result


def get_evaluation(eid: str):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM evaluations WHERE id=?", (eid,)).fetchone()
    if not row:
        return None
    d = _row(row)
    d["passed"] = bool(d["passed"])
    return d


def mark_eval_coaching_linked(eid: str):
    with get_conn() as conn:
        conn.execute("UPDATE evaluations SET coaching_linked=1 WHERE id=?", (eid,))


def get_failed_unlinked_evaluations():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM evaluations WHERE coaching_required=1 AND coaching_linked=0 ORDER BY call_date DESC"
        ).fetchall()
    result = []
    for r in rows:
        d = _row(r)
        d["passed"] = bool(d["passed"])
        result.append(d)
    return result


# ══════════════════════════════════════════════════════════════════════════════
#  COACHING SESSIONS
# ══════════════════════════════════════════════════════════════════════════════

def save_coaching_session(record: dict) -> str:
    cid = record.get("id") or f"CSN-{str(uuid.uuid4())[:6].upper()}"
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO coaching_sessions
               (id,related_eval_id,coaching_date,coaching_type,status,advisor_name,agent_id,team_lead,
                coach_name,department,qa_score,result,topic,no_go_violations,strengths,improvements,
                root_causes_json,improvement_goals,actions_required,training_assigned,follow_up_date,
                completion_status,agent_feedback,commitment,acknowledged,created_at,created_by)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                cid,
                record.get("related_eval_id") or None,
                str(record.get("coaching_date","")),
                record.get("coaching_type",""),
                record.get("status","Scheduled"),
                record.get("advisor_name",""),
                record.get("agent_id",""),
                record.get("team_lead",""),
                record.get("coach_name",""),
                record.get("department",""),
                float(record.get("qa_score",0)),
                record.get("result","FAIL"),
                record.get("topic",""),
                record.get("no_go_violations","None"),
                record.get("strengths",""),
                record.get("improvements",""),
                json.dumps(record.get("root_causes",[])),
                record.get("improvement_goals",""),
                record.get("actions_required",""),
                record.get("training_assigned",""),
                str(record.get("follow_up_date","")),
                record.get("completion_status","Pending Agent"),
                record.get("agent_feedback",""),
                record.get("commitment",""),
                1 if record.get("acknowledged") else 0,
                str(record.get("created_at", date.today())),
                record.get("created_by",""),
            )
        )
    return cid


def get_all_coaching_sessions():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM coaching_sessions ORDER BY coaching_date DESC").fetchall()
    result = []
    for r in rows:
        d = _row(r)
        d["acknowledged"] = bool(d.get("acknowledged", 0))
        d["root_causes"] = d.get("root_causes", [])
        result.append(d)
    return result


def update_coaching_status(cid: str, status: str):
    with get_conn() as conn:
        conn.execute("UPDATE coaching_sessions SET completion_status=? WHERE id=?", (status, cid))


# ══════════════════════════════════════════════════════════════════════════════
#  AUDIT LOGS
# ══════════════════════════════════════════════════════════════════════════════

def log_audit(action: str, detail: str, user_name="System", user_role="—",
              ip="127.0.0.1", session_id=None):
    lid = str(uuid.uuid4())[:8].upper()
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO audit_logs (id,timestamp,user_name,user_role,action,detail,ip_address,session_id)
               VALUES (?,?,?,?,?,?,?,?)""",
            (lid, datetime.now().isoformat(), user_name, user_role,
             action, detail, ip, session_id)
        )
    return lid


def get_audit_logs(limit=500):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT ?", (limit,)
        ).fetchall()
    return _rows(rows)


# ══════════════════════════════════════════════════════════════════════════════
#  SETTINGS
# ══════════════════════════════════════════════════════════════════════════════

def get_setting(key: str, default=None):
    with get_conn() as conn:
        row = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    return row["value"] if row else default


def set_setting(key: str, value: str, updated_by="System"):
    with get_conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO settings (key, value, updated_at, updated_by) VALUES (?,?,?,?)",
            (key, str(value), datetime.now().isoformat(), updated_by)
        )


def get_all_settings():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM settings").fetchall()
    return {r["key"]: r["value"] for r in rows}
