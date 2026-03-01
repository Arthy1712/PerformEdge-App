import streamlit as st
import sqlite3
import hashlib
import pandas as pd

# ----------------------------
# CONFIG
# ----------------------------
DB_PATH = "users.db"
FINAL_DATA_PATH = "final_data.csv"  # Your employee performance CSV

# ----------------------------
# PASSWORD HASH FUNCTION
# ----------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ----------------------------
# GET USER FROM DB
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

    # Ensure employee_id is integer
    if employee_id is not None:
        employee_id = int(employee_id)

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
# FETCH MANAGER TEAM FROM CSV
# ----------------------------
def get_manager_team(manager_emp_id):
    df = pd.read_csv(FINAL_DATA_PATH)
    team_df = df[df["Manager_ID"] == manager_emp_id]
    # Exclude manager themselves if present
    team_df = team_df[team_df["EmpID"] != manager_emp_id]
    return team_df

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
            st.rerun()
        else:
            st.error("Invalid Username or Password")

# ----------------------------
# DASHBOARD AFTER LOGIN
# ----------------------------
else:
    st.sidebar.write(f"👤 Logged in as: {st.session_state.role}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.employee_id = None
        st.rerun()

    st.title("📊 PerformEdge Dashboard")

    # ----------------------------
    # MANAGER DASHBOARD
    # ----------------------------
    if st.session_state.role == "Manager":
        manager_id = st.session_state.employee_id
        team_df = get_manager_team(manager_id)

        st.subheader("👥 Your Team")
        st.dataframe(team_df)

        if "Performance_Score" in team_df.columns:
            top3 = team_df.nlargest(3, "Performance_Score")
            st.subheader("🏆 Top 3 Performers")
            st.dataframe(top3)

    # ----------------------------
    # EMPLOYEE DASHBOARD
    # ----------------------------
    elif st.session_state.role == "Employee":
        emp_id = st.session_state.employee_id
        df = pd.read_csv(FINAL_DATA_PATH)
        emp_df = df[df["EmpID"] == emp_id]

        st.subheader("📋 Your Performance")
        st.dataframe(emp_df)

    # ----------------------------
    # OTHER ROLES (HR / Admin)
    # ----------------------------
    else:
        st.subheader("⚙️ All Data")
        df = pd.read_csv(FINAL_DATA_PATH)
        st.dataframe(df)
