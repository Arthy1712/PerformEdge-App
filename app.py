import streamlit as st
import sqlite3
import hashlib
import streamlit.components.v1 as components
import time

# ----------------------------
# CONFIG
# ----------------------------
DB_PATH = "users.db"
HR_TABLEAU_URL = "https://public.tableau.com/views/PerformEdge-FinalDashboard/Dashboard1"
MANAGER_TABLEAU_URL = "https://public.tableau.com/views/PerformEdge-FinalDashboard/Dashboard2"
EMPLOYEE_TABLEAU_URL = "https://public.tableau.com/views/PerformEdge-FinalDashboard/Dashboard3"

# ----------------------------
# CUSTOM CSS
# ----------------------------
def add_bg_and_style():
    st.markdown(
        """
        <style>

        /* Remove extra spacing */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }

        /* 🔥 GRADIENT BACKGROUND */
        .stApp {
            background: linear-gradient(135deg, #74ebd5, #4facfe);
            height: 100vh;
            overflow: hidden;
        }

        /* COMPANY TITLE */
        .company-title {
            text-align: center;
            font-size: 52px;
            font-weight: 800;
            color: #1f2d3d;
            margin-bottom: 5px;
        }

        /* SUBTITLE */
        .company-subtitle {
            text-align: center;
            font-size: 16px;
            font-weight: 500;
            color: #2c3e50;
            margin-bottom: 25px;
        }

        /* LOGIN AREA */
        .login-container {
            width: 60%;
            margin: auto;
            margin-top: 10px;
        }

        /* FORM BOX */
        .form-box {
            background: rgba(255, 255, 255, 0.85);
            padding: 25px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }

        /* LABEL */
        .form-label {
            font-size: 14px;
            font-weight: 600;
            color: #2c3e50;
        }

        /* INPUT */
        input {
            border-radius: 10px !important;
            padding: 10px !important;
            margin-bottom: 10px;
        }

        /* BUTTON */
        .stButton>button {
            border-radius: 10px;
            background-color: #ffffff;
            color: #2c3e50;
            padding: 8px 20px;
            font-weight: 600;
            border: 1px solid #ccc;
        }

        .stButton>button:hover {
            background-color: #f0f0f0;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

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
    timestamp = int(time.time())

    if role == "Manager":
        url = f"{MANAGER_TABLEAU_URL}?:embed=true&:showVizHome=no&EmpID={emp_id}&_ts={timestamp}"
    elif role == "Employee":
        url = f"{EMPLOYEE_TABLEAU_URL}?:embed=true&:showVizHome=no&EmpID={emp_id}&_ts={timestamp}"
    else:
        url = f"{HR_TABLEAU_URL}?:embed=true&:showVizHome=no&_ts={timestamp}"

    components.html(
        f'<iframe src="{url}" width="100%" height="1000" style="border:none;"></iframe>',
        height=1400,
    )

# ----------------------------
# LOGIN PAGE
# ----------------------------
if not st.session_state.logged_in:

    add_bg_and_style()

    # 🔥 HEADER
    st.markdown('<div class="company-title">ABC Technologies</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="company-subtitle">PerformEdge - Employee Performance Evaluation System</div>',
        unsafe_allow_html=True
    )

    # LOGIN FORM
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="form-box">', unsafe_allow_html=True)

    st.markdown('<div class="form-label">Username</div>', unsafe_allow_html=True)
    username = st.text_input("", placeholder="Enter your username")

    st.markdown('<div class="form-label">Password</div>', unsafe_allow_html=True)
    password = st.text_input("", type="password", placeholder="Enter your password")

    if st.button("Login"):
        success, role, employee_id = login(username, password)
        if success:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.session_state.employee_id = employee_id
            st.rerun()
        else:
            st.error("Invalid Username or Password")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

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

    show_tableau_dashboard()
