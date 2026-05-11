"""
Authentication & Session Management — Production (SQLite-backed)
"""

import streamlit as st
import uuid
from datetime import datetime
from config.settings import ROLES
from utils.database import (authenticate_user, log_audit, get_all_users,
                             get_failed_unlinked_evaluations, get_all_coaching_sessions,
                             get_all_evaluations, get_audit_logs)


def init_session():
    defaults = {
        "authenticated": False,
        "user": None,
        "session_id": None,
        "login_attempts": 0,
        "last_activity": None,
        "current_page": "Executive Dashboard",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def authenticate(email: str, password: str) -> tuple[bool, str]:
    if st.session_state.login_attempts >= 5:
        return False, "Account locked — too many failed attempts."
    user = authenticate_user(email, password)
    if not user:
        st.session_state.login_attempts += 1
        return False, "Invalid email or password."
    st.session_state.authenticated = True
    st.session_state.user = user
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.last_activity = datetime.now()
    st.session_state.login_attempts = 0
    log_audit("LOGIN", f"User {user['name']} logged in",
              user_name=user["name"], user_role=user.get("role","—"),
              session_id=st.session_state.session_id)
    return True, "Login successful"


def logout():
    user = st.session_state.get("user") or {}
    log_audit("LOGOUT", f"User {user.get('name','?')} logged out",
              user_name=user.get("name","?"), user_role=user.get("role","—"),
              session_id=st.session_state.get("session_id"))
    for key in ["authenticated","user","session_id","last_activity"]:
        st.session_state[key] = None if key != "authenticated" else False
    st.rerun()


def require_auth(role: str = None):
    if not st.session_state.get("authenticated"):
        st.error("Access denied — please log in.")
        st.stop()
    if role and st.session_state.user.get("role") != role:
        st.error("You don't have permission to view this page.")
        st.stop()


def current_user():
    return st.session_state.get("user") or {}


def has_role(*roles):
    user = current_user()
    return user.get("role") in roles or user.get("role") == "super_admin"


def log_action(action: str, detail: str):
    user = current_user()
    log_audit(action, detail,
              user_name=user.get("name","System"),
              user_role=user.get("role","—"),
              session_id=st.session_state.get("session_id"))


# Convenience loaders for pages
def load_evaluations():
    return get_all_evaluations()

def load_coaching_sessions():
    return get_all_coaching_sessions()

def load_audit_logs():
    return get_audit_logs()

def load_users():
    return get_all_users()

def load_failed_unlinked():
    return get_failed_unlinked_evaluations()
