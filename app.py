import streamlit as st
import sqlite3
import hashlib
import streamlit.components.v1 as components

# ----------------------------
# CONFIG
# ----------------------------
DB_PATH = "users.db"

# 🔁 PASTE YOUR TABLEAU PUBLIC URL BELOW
BASE_TABLEAU_URL = "https://public.tableau.com/views/PerformEdge_Dashboard/EmpPerfAnalyticsDashboard?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"

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
    role = st.session_state.role
    emp_id = st.session_state.employee_id

    # Build dynamic URL based on role
    if role == "Employee":
        tableau_url = f"{BASE_TABLEAU_URL}?EmpID={emp_id}"

    elif role == "Manager":
        tableau_url = f"{BASE_TABLEAU_URL}?Manager_ID={emp_id}"

    else:  # Admin & HR
        tableau_url = BASE_TABLEAU_URL

    components.iframe(tableau_url, height=900, scrolling=True)

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
