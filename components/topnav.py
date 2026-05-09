"""
Top Navigation Bar Component
Modern enterprise top navigation replacing the old sidebar.
"""

import streamlit as st
from utils.auth import current_user, logout, has_role
from config.settings import ROLES


# Navigation structure mapped to roles
NAV_STRUCTURE = [
    {
        "group": "Dashboards",
        "items": [
            ("Executive Dashboard", "Executive Dashboard", "super_admin,qa_admin,qa_evaluator,team_leader,ops_manager,viewer"),
            ("QA Insights", "QA Insights", "super_admin,qa_admin,qa_evaluator,team_leader,ops_manager,viewer"),
            ("Coaching Insights", "Coaching Insights", "super_admin,qa_admin,team_leader,coach,ops_manager,viewer"),
            ("Agent Performance", "Agent Performance", "super_admin,qa_admin,team_leader,ops_manager,agent,viewer"),
            ("Root Cause Analysis", "Root Cause Analysis", "super_admin,qa_admin,ops_manager"),
        ],
    },
    {
        "group": "Evaluations",
        "items": [
            ("New Evaluation", "New Evaluation", "super_admin,qa_admin,qa_evaluator"),
            ("Evaluations List", "Evaluations List", "super_admin,qa_admin,qa_evaluator,team_leader,ops_manager"),
        ],
    },
    {
        "group": "Coaching",
        "items": [
            ("New Coaching Session", "New Coaching Session", "super_admin,qa_admin,team_leader,coach"),
            ("Coaching Sessions", "Coaching Sessions", "super_admin,qa_admin,team_leader,coach,ops_manager"),
        ],
    },
    {
        "group": "Reports",
        "items": [
            ("Reports & Export", "Reports & Export", "super_admin,qa_admin,qa_evaluator,team_leader,ops_manager,viewer"),
        ],
    },
    {
        "group": "Administration",
        "items": [
            ("User Management", "User Management", "super_admin,qa_admin"),
            ("Form Builder", "Form Builder", "super_admin,qa_admin"),
            ("System Settings", "System Settings", "super_admin"),
            ("Audit Logs", "Audit Logs", "super_admin,qa_admin"),
        ],
    },
]


def get_navigation_items(user_role: str) -> list:
    """Get navigation items filtered by user role."""
    items = []
    for group in NAV_STRUCTURE:
        group_items = []
        for item_key, item_label, roles in group["items"]:
            if user_role == "super_admin" or user_role in roles.split(","):
                group_items.append((item_key, item_label))
        if group_items:
            items.append((group["group"], group_items))
    return items


def render_topnav():
    """Render the modern top navigation bar."""
    user = current_user()
    role = user.get("role", "viewer")
    role_cfg = ROLES.get(role, {})
    
    # Get navigation items for this role
    nav_items = get_navigation_items(role)
    current_page = st.session_state.get("current_page", "Executive Dashboard")
    
    # Flatten navigation to get all items
    all_items = []
    for group_name, group_items in nav_items:
        all_items.extend(group_items)
    
    # Build the logo and user section HTML
    user_avatar = user.get("avatar", user.get("name", "U")[0].upper() if user.get("name") else "U")
    user_name = user.get("name", "User")
    user_role_label = role_cfg.get("label", role)
    
    # Use CSS-based navigation with radio buttons
    nav_options = [item[0] for item in all_items]
    nav_labels = [item[1] for item in all_items]
    
    # Try to get index of current page
    try:
        default_idx = nav_options.index(current_page) if current_page in nav_options else 0
    except (ValueError, IndexError):
        default_idx = 0
    
    # Render the HTML navigation bar
    st.markdown(
        """
        <style>
        .udrive-topnav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 64px;
            background: #FFFFFF;
            border-bottom: 1px solid #E2E8F0;
            display: flex;
            align-items: center;
            padding: 0 1.5rem;
            z-index: 9999;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        .udrive-logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 800;
            font-size: 1.125rem;
            color: #1A1E3C;
            flex-shrink: 0;
        }
        
        .udrive-logo-icon {
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, #7C3AED, #6D28D9);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 800;
            font-size: 1rem;
        }
        
        .udrive-nav-items {
            display: flex;
            align-items: center;
            gap: 0.25rem;
            margin-left: 2rem;
            flex-wrap: wrap;
        }
        
        .udrive-nav-item {
            padding: 0.5rem 1rem;
            border-radius: 10px;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.875rem;
            font-weight: 600;
            color: #64748B;
            cursor: pointer;
            transition: all 0.15s ease;
            white-space: nowrap;
        }
        
        .udrive-nav-item:hover {
            background: #F1F5F9;
            color: #1E293B;
        }
        
        .udrive-nav-item.active {
            background: rgba(124, 58, 237, 0.1);
            color: #7C3AED;
        }
        
        .udrive-user {
            margin-left: auto;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .udrive-user-avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: linear-gradient(135deg, #06B6D4, #7C3AED);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 700;
            font-size: 0.875rem;
        }
        
        .udrive-user-info {
            text-align: right;
        }
        
        .udrive-user-name {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.875rem;
            font-weight: 600;
            color: #1E293B;
        }
        
        .udrive-user-role {
            font-size: 0.75rem;
            color: #94A3B8;
        }
        
        .udrive-content {
            padding-top: 80px;
            padding-left: 2rem;
            padding-right: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Hide default Streamlit header */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        
        /* Main content spacing */
        .block-container {
            padding-top: 1rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # Logo and brand
    st.markdown(
        f"""
        <div class="udrive-topnav">
            <div class="udrive-logo">
                <div class="udrive-logo-icon">U</div>
                <span>UDrive Monitor</span>
            </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Build navigation as clickable buttons for each section
    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    cols = [col1, col2, col3, col4, col5]
    
    # Render each navigation item as a clickable element
    items_per_col = (len(all_items) + 4) // 5
    
    # Group navigation items
    grouped_nav = []
    for i in range(0, len(all_items), items_per_col):
        grouped_nav.append(all_items[i:i+items_per_col])
    
    # Use columns for navigation
    with st.container():
        nav_cols = st.columns(len(all_items[:6]))
        for i, (item_key, item_label) in enumerate(all_items[:6]):
            if i < len(nav_cols):
                with nav_cols[i]:
                    is_active = item_key == current_page
                    if st.button(
                        item_label,
                        key=f"nav_{item_key}",
                        type="primary" if is_active else "secondary",
                        use_container_width=True
                    ):
                        st.session_state.current_page = item_key
                        st.rerun()
    
    # Close topnav div
    st.markdown("</div>", unsafe_allow_html=True)
    
    # User section at the right
    with st.container():
        u_col1, u_col2, u_col3 = st.columns([1, 1, 1])
        with u_col2:
            st.markdown(
                f"""
                <div class="udrive-user" style="position:fixed; right:2rem; top:0.75rem;">
                    <div style="text-align:right; margin-right:0.5rem;">
                        <div class="udrive-user-name">{user_name}</div>
                        <div class="udrive-user-role">{user_role_label}</div>
                    </div>
                    <div class="udrive-user-avatar">{user_avatar}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with u_col3:
            if st.button("Sign Out", key="topnav_logout", use_container_width=True):
                logout()
    
    # Main content wrapper
    st.markdown('<div class="udrive-content">', unsafe_allow_html=True)


def render_topnav_end():
    """Close the main content wrapper."""
    st.markdown('</div>', unsafe_allow_html=True)