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
# PREMIUM CSS + ANIMATION
# ----------------------------
st.markdown("""
<style>

/* FULL CENTER */
.main {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #dbeafe, #bfdbfe, #93c5fd);
}

/* Remove padding */
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}

/* Glass Card */
.login-box {
    background: rgba(255, 255, 255, 0.85);
    padding: 40px;
    border-radius: 18px;
    width: 420px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    backdrop-filter: blur(10px);

    animation: fadeSlide 1s ease;
}

/* Title */
.company-title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    color: #0F172A;
}

/* Subtitle */
.subtitle {
    font-size: 18px;
    text-align: center;
    color: #1e293b;
    margin-bottom: 15px;
}

/* Animated Employee Icon */
.icon {
    font-size: 40px;
    text-align: center;
    animation: float 2s ease-in-out infinite;
    margin-bottom: 15px;
}

/* Button */
div.stButton > button {
    background-color: #1d4ed8;
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

div.stButton > button:hover {
    background-color: #1e40af;
    transform: scale(1.05);
}

/* Animations */
@keyframes fadeSlide {
    from {
        opacity: 0;
        transform: translateY(40px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
    100% { transform: translateY(0px); }
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

    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    st.markdown('<div class="company-title">ABC Technologies</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Employee Performance Evaluation System</div>', unsafe_allow_html=True)
    st.markdown('<div class="icon">👨‍💼</div>', unsafe_allow_html=True)

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
