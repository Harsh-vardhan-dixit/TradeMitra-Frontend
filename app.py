import streamlit as st
import requests
from monitor_page import start_monitoring
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE = os.getenv('api-base')  # Change this to your FastAPI backend URL
# API_BASE = st.secrets["API_BASE"]

st.set_page_config(page_title="Auth App", page_icon="🔒")

# Session state to handle navigation
if "page" not in st.session_state:
    st.session_state.page = "login"

def go_to(page):
    st.session_state.page = page
    st.rerun()


def register_page():
    st.title("🔐 Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if username and password:
            response = requests.post(f"{API_BASE}/register", json={"username": username, "password": password})
            if response.status_code == 200:
                st.success("✅ Registration successful! Please login.")
                go_to("login")
            else:
                st.error(response.json().get("detail", "Registration failed"))
        else:
            st.warning("Please fill all fields.")

    st.button("Already have an account? Login", on_click=lambda: go_to("login"))

def login_page():
    st.title("🔑 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            response = requests.post(f"{API_BASE}/login", json={"username": username, "password": password})
            if response.status_code == 200:
                st.session_state["username"] = username
                response_data = response.json()
                user_info = response_data.get('data', {})
                st.session_state["user_id"] = user_info.get('user_id')
                go_to("dashboard")
            else:
                try:
                    error_data = response.json()
                    st.error(error_data.get("detail", "Login failed"))
                except requests.exceptions.JSONDecodeError:
                    st.error("Login failed: Invalid response from server")
        else:
            st.warning("Please enter your username and password.")

    st.button("Don't have an account? Register", on_click=lambda: go_to("register"))

def dashboard_page():

    st.title(f"👋 Welcome, {st.session_state['username']}!")
    st.write("This is your dashboard page.")

    # Initialize session state (must be inside this page)
    if "validated" not in st.session_state:
        st.session_state.validated = False
        st.session_state.response = None

    st.title("Send Token and Client ID")

    token = st.text_input("Enter your token")
    client_id = st.text_input("Enter Client ID")

    if st.button("Validate Token"):
        url = f"{API_BASE}/validate-token"
        json_data = {"token": token,"client_id":client_id}

        response = requests.post(url, json=json_data)
        st.session_state.response = response.json()
        st.session_state.validated = True

    # ⬇️ Now SAFE to check validated state
    if st.session_state.validated:
        st.write("Response:")
        st.json(st.session_state.response)

        st.text("Is this retrieved information correct?")

        if st.button("YES"):
            st.session_state.token = token
            st.session_state.client_id = client_id
            st.success("Starting Monitoring...")
            go_to("start_monitoring")

        if st.button("NO"):
            st.warning("Please enter the token again.")
            st.session_state.validated = False



# def start_monitoring():
#     st.title(f"Let's Start Monitoring 🧑‍🦱 !{st.session_state['username']}")
    
    
# Page routing
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "register":
    register_page()
elif st.session_state.page == "dashboard":
    dashboard_page()
elif st.session_state.page == "start_monitoring":
    start_monitoring()
    
