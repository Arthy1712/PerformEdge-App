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
st.markdown("""
<style>

/* FULL PAGE CENTERING */
.main {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 10vh;
}

/* Reduce page padding */
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}

/* Pale Green Background */
.stApp {
    background: linear-gradient(135deg, #d8f3dc, #b7e4c7, #95d5b2);
}

/* Font */
html, body, [class*="css"]  {
    font-family: 'Segoe UI', sans-serif;
}

/* Login Card */
.login-box {
    background: white;
    padding: 35px;
    border-radius: 15px;
    width: 400px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.15);
}

/* Company Title */
.company-title {
    font-size: 42px;
    font-weight: bold;
    color: black;
    text-align: center;
}

/* Subtitle */
.subtitle {
    font-size: 20px;
    color: black;
    text-align: center;
    margin-bottom: 10px;
}

/* Icon */
.icon {
    font-size: 32px;
    text-align: center;
    margin-bottom: 10px;
}

/* Button Styling */
div.stButton > button {
    background-color: #0F4C81;
    color: white;
    border-radius: 8px;
    height: 45px;
    width: 100%;
    font-weight: bold;
    border: none;
}

div.stButton > button:hover {
    background-color: #092f4c;
}

</style>
""", unsafe_allow_html=True)

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
        f'<iframe src="{url}" width="100%" height="900" style="border:none;"></iframe>',
        height=1000,
    )

# ----------------------------
# LOGIN PAGE
# ----------------------------
if not st.session_state.logged_in:

    st.markdown('<div class="main">', unsafe_allow_html=True)

    st.markdown('<div class="company-title">ABC Technologies</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Employee Performance Evaluation System</div>', unsafe_allow_html=True)
    st.markdown('<div class="icon">👨‍💼 PerformEdge - Login</div>', unsafe_allow_html=True)

    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    if st.button("Login"):
        success, role, employee_id = login(username, password)
        if success:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.session_state.employee_id = employee_id
            st.rerun()
        else:
            st.error("❌ Invalid Username or Password")

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
