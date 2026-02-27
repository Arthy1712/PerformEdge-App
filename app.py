import streamlit as st
import sqlite3
import hashlib
import pandas as pd

# ----------------------------
# CONFIG
# ----------------------------
DB_PATH = "users.db"

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
# DASHBOARD AFTER LOGIN
# ----------------------------
else:
    
    st.sidebar.write(f"Logged in as: {st.session_state.role}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.employee_id = None
        st.rerun()

    st.title("📊 PerformEdge Dashboard")

    # ----------------------------
    # ROLE BASED ACCESS
    # ----------------------------
    role = st.session_state.role

    if role == "Admin":
        st.subheader("Admin Panel")
        st.write("• Full system access")
        st.write("• Manage users")
        st.write("• View all employees")
        
    elif role == "HR":
        st.subheader("HR Panel")
        st.write("• View all employee performance")
        st.write("• Generate reports")

    elif role == "Manager":
        st.subheader("Manager Panel")
        st.write("• View team members")
        st.write("• Team analytics")

    elif role == "Employee":
        st.subheader("Employee Panel")
        st.write("• View your performance")
        st.write(f"Your Employee ID: {st.session_state.employee_id}")
