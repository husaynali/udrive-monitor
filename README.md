# QA Pro Platform — Production Release

A fully production-ready QA Evaluation, Coaching & Performance Management platform built with Streamlit + SQLite.

## What changed (Demo → Production)

| Area | Before | After |
|------|--------|-------|
| Data storage | `st.session_state` (wiped on refresh) | SQLite database (`data/qa_platform.db`) |
| Users | Hard-coded dict in `auth.py` | `users` table with hashed passwords |
| Evaluations | In-memory list | `evaluations` table with full indexing |
| Coaching sessions | In-memory list | `coaching_sessions` table |
| Audit logs | In-memory list | `audit_logs` table (persisted forever) |
| Settings | Hard-coded constants | `settings` table (editable via UI) |
| User management | Session only | Full CRUD — create, role-change, deactivate |

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

The database is created automatically at `data/qa_platform.db` on first run and seeded with 60 demo evaluations and 5 demo users.

## Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| Super Admin | admin@qa-pro.com | Admin@123 |
| QA Evaluator | evaluator@qa-pro.com | Eval@123 |
| Coach | coach@qa-pro.com | Coach@123 |
| Agent | agent@qa-pro.com | Agent@123 |
| Ops Manager | manager@qa-pro.com | Mgr@123 |

## Project Structure

```
qa_platform/
├── app.py                    # Entry point — boots DB, routes pages
├── data/
│   └── qa_platform.db        # SQLite database (auto-created)
├── utils/
│   ├── database.py           # ★ NEW — full DB layer (schema + all CRUD)
│   ├── auth.py               # Updated — authenticates via DB
│   └── theme.py              # Unchanged
├── pages/
│   ├── evaluation_form.py    # Saves to DB
│   ├── evaluations_list.py   # Reads from DB
│   ├── coaching_form.py      # Saves to DB, marks eval linked
│   ├── coaching_list.py      # Reads from DB
│   ├── admin_users.py        # Full CRUD via DB
│   ├── admin_settings.py     # Settings persisted to DB
│   ├── audit_logs.py         # Reads from DB
│   └── dashboard_*.py        # All read from DB
├── config/settings.py        # Constants (unchanged)
└── requirements.txt
```

## Database Schema

- **users** — authentication, roles, departments
- **evaluations** — full QA scorecard records
- **coaching_sessions** — coaching records linked to evaluations
- **audit_logs** — every login, create, update action
- **settings** — platform configuration (thresholds, SLAs, flags)
