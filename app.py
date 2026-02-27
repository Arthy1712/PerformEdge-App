import streamlit as st
import pandas as pd
import numpy as np
import joblib

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="PerformEdge", layout="wide")

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("Final_Data.csv")

df = load_data()

# -----------------------------
# Load Model
# -----------------------------
model = joblib.load("model.pkl")

# -----------------------------
# Dummy Users (Role-Based Access)
# -----------------------------
users = {
    "admin": {"password": "admin123", "role": "Admin"},
    "hr": {"password": "hr123", "role": "HR"},
    "lead": {"password": "lead123", "role": "Team Lead"},
    "emp": {"password": "emp123", "role": "Employee"}
}

# -----------------------------
# Login System
# -----------------------------
st.title("🔐 PerformEdge - Performance Management System")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.role = users[username]["role"]
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

# -----------------------------
# After Login
# -----------------------------
else:
    role = st.session_state.role
    st.sidebar.success(f"Logged in as: {role}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # -------------------------
    # ADMIN DASHBOARD
    # -------------------------
    if role == "Admin":
        st.header("📊 Admin Dashboard")
        st.write("Full Dataset Access")
        st.dataframe(df)

        st.write("Dataset Shape:", df.shape)

    # -------------------------
    # HR DASHBOARD
    # -------------------------
    elif role == "HR":
        st.header("👩‍💼 HR Dashboard")
        st.write("Summary Statistics")
        st.dataframe(df.describe())

    # -------------------------
    # TEAM LEAD DASHBOARD
    # -------------------------
    elif role == "Team Lead":
        st.header("👨‍💻 Team Lead Dashboard")
        st.write("First 20 Records")
        st.dataframe(df.head(20))

    # -------------------------
    # EMPLOYEE DASHBOARD
    # -------------------------
    elif role == "Employee":
        st.header("👤 Employee Dashboard")
        st.write("Limited Access View")
        st.dataframe(df.sample(5))

    # -------------------------
    # Prediction Section (All Roles)
    # -------------------------
    st.markdown("---")
    st.subheader("🔮 Make New Prediction")

    feature_columns = df.columns[:-1]  # assuming last column is target
    input_data = []

    cols = st.columns(3)

    for i, col in enumerate(feature_columns):
        with cols[i % 3]:
            val = st.number_input(f"{col}", value=0.0)
            input_data.append(val)

    if st.button("Predict Performance"):
        prediction = model.predict([input_data])[0]
        st.success(f"Prediction Result: {prediction}")
