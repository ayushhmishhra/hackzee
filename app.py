import streamlit as st

from database import init_db
from backend.auth import signup_user, login_user
from backend.logic import run_solution
from utils.helpers import clean_text, format_result


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="HackZee",
    page_icon="⚡",
    layout="centered"
)


# ---------------- DATABASE ----------------

init_db()


# ---------------- SESSION STATE ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# ---------------- DARK THEME ----------------

st.markdown(
    """
    <style>
    .stApp {
        background-color: #101010;
        color: #FFFFFF;
    }

    [data-testid="stHeader"] {
        background-color: #101010;
    }

    .block-container {
        padding-top: 2rem;
        max-width: 750px;
    }

    h1, h2, h3, p, label {
        color: #FFFFFF !important;
    }

    div.stButton > button {
        background-color: #1DB954;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }

    div.stButton > button:hover {
        background-color: #169c46;
        color: white;
    }

    input, textarea {
        background-color: #222222 !important;
        color: white !important;
    }

    [data-testid="stForm"] {
        background-color: #181818;
        padding: 20px;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------- HEADER ----------------

st.title("⚡ HackZee")
st.caption("Your reusable AI-powered hackathon starter template.")


# ---------------- LOGOUT ----------------

if st.session_state.logged_in:
    user = st.session_state.user

    st.success(f"Welcome, {user['name']}!")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    st.divider()

    st.subheader("🚀 Problem Solver")
    st.write("Enter your problem or text below.")

    with st.form("problem_form"):
        user_input = st.text_area(
            "Your input",
            placeholder="Describe your problem here..."
        )

        submitted = st.form_submit_button("Run Solution")

    if submitted:
        user_input = clean_text(user_input)

        result = run_solution(user_input)

        if result["success"]:
            st.subheader("Result")
            st.write(format_result(result["result"]))
        else:
            st.warning(result["result"])


# ---------------- LOGIN / SIGNUP ----------------

else:
    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    # LOGIN FORM
    with login_tab:
        st.subheader("Welcome Back")

        with st.form("login_form"):
            login_email = st.text_input("Email")
            login_password = st.text_input(
                "Password",
                type="password"
            )

            login_submitted = st.form_submit_button("Login")

        if login_submitted:
            if not login_email.strip() or not login_password:
                st.error("Please enter your email and password.")
            else:
                success, message, user = login_user(
                    login_email,
                    login_password
                )

                if success:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error(message)

    # SIGNUP FORM
    with signup_tab:
        st.subheader("Create Your Account")

        with st.form("signup_form"):
            signup_name = st.text_input("Full Name")
            signup_email = st.text_input("Email Address")
            signup_password = st.text_input(
                "Create Password",
                type="password",
                help="At least 8 characters, with uppercase, lowercase, number and special character."
            )

            signup_submitted = st.form_submit_button("Create Account")

        if signup_submitted:
            success, message = signup_user(
                signup_name,
                signup_email,
                signup_password
            )

            if success:
                st.success(message)
                st.info("Now open the Login tab and sign in.")
            else:
                st.error(message)