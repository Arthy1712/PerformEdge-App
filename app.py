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
# CUSTOM CSS (UPDATED)
# ----------------------------
st.markdown("""
<style>

/* Reduce overall page spacing */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 1rem !important;
}

/* Font */
html, body, [class*="css"]  {
    font-family: 'Segoe UI', sans-serif;
}

/* Pale Green Background */
.stApp {
    background: linear-gradient(135deg, #d4f5e9, #b7e4c7, #95d5b2);
}

/* Company Title */
.company-title {
    font-size: 40px;
    font-weight: bold;
    color: #1b4332;
    text-align: center;
    margin-top: 10px;
}

/* Subtitle */
.subtitle {
    font-size: 18px;
    color: #2d6a4f;
    text-align: center;
    margin-bottom: 10px;
}

/* Icon + Title */
.icon {
    font-size: 22px;
    text-align: center;
    margin-bottom: 10px;
    color: #1b4332;
}

/* Button Styling */
div.stButton > button {
    background-color: #2d6a4f;
    color: white;
    border-radius: 8px;
    height: 42px;
    width: 100%;
    font-weight: bold;
    border: none;
}

div.stButton > button:hover {
    background-color: #1b4332;
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
        height=900,
    )

# ----------------------------
# LOGIN PAGE
# ----------------------------
if not st.session_state.logged_in:

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
