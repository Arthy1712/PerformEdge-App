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
# PREMIUM UI CSS
# ----------------------------
st.markdown("""
<style>

/* Global Font */
html, body, [class*="css"]  {
    font-family: 'Segoe UI', sans-serif;
}

/* Gradient Background */
.stApp {
    background: linear-gradient(135deg, #0F4C81, #1E3C72, #2A5298);
}

/* Company Title */
.company-title {
    font-size: 46px;
    font-weight: bold;
    color: white;
    text-align: center;
    margin-top: 30px;
    letter-spacing: 1px;
}

/* Subtitle */
.subtitle {
    font-size: 20px;
    color: #e0e0e0;
    text-align: center;
    margin-bottom: 30px;
}

/* Glassmorphism Login Card */
.login-container {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(12px);
    padding: 40px;
    border-radius: 20px;
    width: 360px;
    margin: auto;
    margin-top: 30px;
    box-shadow: 0px 8px 30px rgba(0,0,0,0.3);
    text-align: center;
    border: 1px solid rgba(255,255,255,0.2);
}

/* PerformEdge Title */
.login-title {
    font-size: 22px;
    font-weight: bold;
    color: white;
    margin-bottom: 15px;
}

/* Employee Icon */
.icon {
    font-size: 55px;
    margin-bottom: 10px;
}

/* Input Styling */
div[data-baseweb="input"] input {
    border-radius: 8px !important;
}

/* Button Styling */
div.stButton > button {
    background: linear-gradient(90deg, #00C6FF, #0072FF);
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 100%;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

div.stButton > button:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #0072FF, #00C6FF);
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
        f'<iframe src="{url}" width="100%" height="1000" style="border:none;"></iframe>',
        height=1000,
    )

# ----------------------------
# LOGIN PAGE
# ----------------------------
if not st.session_state.logged_in:

    # Company Title
    st.markdown('<div class="company-title">ABC Technologies</div>', unsafe_allow_html=True)

    # Subtitle
    st.markdown('<div class="subtitle">Employee Performance Evaluation System</div>', unsafe_allow_html=True)

    # Login Card Start
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    # Icon
    st.markdown('<div class="icon">👨‍💼</div>', unsafe_allow_html=True)

    # PerformEdge Title (NEW)
    st.markdown('<div class="login-title">📊 PerformEdge Login</div>', unsafe_allow_html=True)

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
