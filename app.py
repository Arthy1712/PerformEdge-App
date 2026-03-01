import streamlit as st
import sqlite3
import hashlib
import streamlit.components.v1 as components

# ----------------------------
# CONFIG
# ----------------------------
DB_PATH = "users.db"

# 🔁 PASTE YOUR TABLEAU PUBLIC URL BELOW
HR_TABLEAU_URL = "https://public.tableau.com/views/PerformEdge_Dashboard/Dashboard1?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"
MANAGER_TABLEAU_URL = "https://public.tableau.com/views/PerformEdge_Dashboard/Dashboard2?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"
# ----------------------------
# PASSWORD HASH FUNCTION
# ----------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ----------------------------
# DATABASE CONNECTION
# ----------------------------
def get_user(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT username, password, role, employee_id FROM users WHERE username=?",
        (username,)
    )
    
    user = cursor.fetchone()
    conn.close()
    return user

# ----------------------------
# LOGIN FUNCTION
# ----------------------------
def login(username, password):
    user = get_user(username)
    
    if user:
        stored_username, stored_password, role, employee_id = user
        
        if hash_password(password) == stored_password:
            return True, role, employee_id
    
    return False, None, None

# ----------------------------
# SESSION STATE INIT
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.employee_id = None

# ----------------------------
# DASHBOARD FUNCTION
# ----------------------------
def show_tableau_dashboard():
    import time

    role = st.session_state.role
    emp_id = str(st.session_state.employee_id)
    timestamp = int(time.time())

    # 🔥 Clean base URL (remove everything after ?)
    if role == "Manager":
        base_url = MANAGER_TABLEAU_URL.split("?")[0]
        url = f"{base_url}?:embed=true&:showVizHome=no&Manager_ID_Param={emp_id}&_ts={timestamp}"

    elif role == "Employee":
        base_url = HR_TABLEAU_URL.split("?")[0]
        url = f"{base_url}?:embed=true&:showVizHome=no&EmpID={emp_id}&_ts={timestamp}"

    else:
        base_url = HR_TABLEAU_URL.split("?")[0]
        url = f"{base_url}?:embed=true&:showVizHome=no&_ts={timestamp}"

    st.write("DEBUG URL:", url)

    iframe = f"""
        <iframe src="{url}"
        width="100%"
        height="900"
        frameborder="0">
        </iframe>
    """

    components.html(iframe, height=900)
# ----------------------------
# LOGIN PAGE
# ----------------------------
if not st.session_state.logged_in:
    
    st.title("🔐 PerformEdge Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        success, role, employee_id = login(username, password)
        
        if success:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.session_state.employee_id = employee_id
            st.success(f"Welcome {role}!")
            st.rerun()
        else:
            st.error("Invalid Username or Password")

# ----------------------------
# AFTER LOGIN
# ----------------------------
else:
    
    st.sidebar.write(f"👤 Logged in as: {st.session_state.role}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.employee_id = None
        st.rerun()

    st.title("📊 PerformEdge Dashboard")

    show_tableau_dashboard()
