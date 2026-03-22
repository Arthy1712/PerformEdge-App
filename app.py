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
        .stApp {
            background: linear-gradient(to right, #1f4037, #99f2c8);
        }

        .login-container {
            background-color: white;
            padding: 40px;
            border-radius: 15px;
            width: 350px;
            margin: auto;
            margin-top: 100px;
            box-shadow: 0px 8px 20px rgba(0,0,0,0.2);
            text-align: center;
        }

        .login-title {
            font-size: 26px;
            font-weight: bold;
            color: #1f4037;
        }

        .login-subtitle {
            font-size: 14px;
            color: gray;
            margin-bottom: 15px;
        }

        input {
            border-radius: 8px !important;
            border: 1px solid #ccc !important;
            padding: 10px !important;
        }

        .stButton>button {
            width: 100%;
            border-radius: 10px;
            background-color: #1f4037;
            color: white;
            font-weight: bold;
            padding: 10px;
        }

        .stButton>button:hover {
            background-color: #14532d;
            color: white;
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

    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    # 🔥 UPDATED BRANDING
    st.markdown('<div class="login-title">ABC Technologies</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="login-subtitle">PerformEdge - Employee Performance Evaluation System</div>',
        unsafe_allow_html=True
    )

    # Logo
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)

    # Inputs
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Login button
    if st.button("Login"):
        success, role, employee_id = login(username, password)
        if success:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.session_state.employee_id = employee_id
            st.rerun()
        else:
            st.error("❌ Invalid Username or Password")

    # Tagline
    st.markdown(
        "<p style='text-align:center; color:gray; font-size:13px;'>Driving Performance • Enabling Growth • Empowering Talent</p>",
        unsafe_allow_html=True
    )

    # Footer
    st.markdown(
        "<p style='text-align:center; font-size:12px; color:gray;'>© 2026 ABC Technologies</p>",
        unsafe_allow_html=True
    )

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
