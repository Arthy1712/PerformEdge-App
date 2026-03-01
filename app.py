import streamlit as st
import sqlite3
import hashlib
import streamlit.components.v1 as components
import time

# ----------------------------
# CONFIG
# ----------------------------
DB_PATH = "users.db"

HR_TABLEAU_URL = "https://public.tableau.com/views/PerformEdge_Dashboard/Dashboard1"
MANAGER_TABLEAU_URL = "https://public.tableau.com/views/PerformEdge_Dashboard/Dashboard2"

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
        (username.strip(),)
    )
    user = cursor.fetchone()
    conn.close()
    return user

# ----------------------------
# LOGIN FUNCTION
# ----------------------------
def login(username, password):
    user = get_user(username)
    if not user:
        return False, None, None

    stored_username, stored_password, role, employee_id = user
    if hash_password(password) != stored_password:
        return False, None, None

    return True, role.strip(), employee_id

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
    timestamp = int(time.time())  # prevent caching

    if role == "Manager":
        url = f"{MANAGER_TABLEAU_URL}?:embed=true&:showVizHome=no&EmpID={emp_id}&_ts={timestamp}"
    elif role == "Employee":
        url = f"{HR_TABLEAU_URL}?:embed=true&:showVizHome=no&EmpID={emp_id}&_ts={timestamp}"
    else:
        url = f"{HR_TABLEAU_URL}?:embed=true&:showVizHome=no&_ts={timestamp}"

    st.write("📌 Dashboard URL being used:")
    st.write(url)

    components.html(
        f'<iframe src="{url}" width="1000" height="1000" style="border:none;"></iframe>',
        height=1400,
    )

# ----------------------------
# LOGIN PAGE
# ----------------------------
if not st.session_state.logged_in:
    st.title("📊 PerformEdge Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        success, role, employee_id = login(username, password)
        if success:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.session_state.employee_id = employee_id
        else:
            st.error("❌ Invalid Username or Password")

# ----------------------------
# AFTER LOGIN
# ----------------------------
else:
    st.sidebar.write(f"👤 Logged in as: {st.session_state.role}")

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.employee_id = None

    # Show dashboard
    show_tableau_dashboard()
