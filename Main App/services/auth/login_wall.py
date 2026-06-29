import streamlit as st
from services.persistence.exercise_repository import (
    register_user,
    login_user
)


def render_login_wall():
    if st.session_state.get("user_id") is not None:
        return True

    st.title("🏋️‍♂️ AI Real-time GYM Trainer")
    st.markdown("### Login or Register")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # ---------------- LOGIN ---------------- #

    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            login_button = st.form_submit_button(
                "Login",
                use_container_width=True
            )

        if login_button:
            if username.strip() == "" or password.strip() == "":
                st.error("Please enter both username and password.")
            else:
                user = login_user(username.strip(), password)

                if user:
                    st.session_state["user_id"] = user["id"]
                    st.session_state["username"] = user["username"]

                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

    # ---------------- REGISTER ---------------- #

    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("Choose Username")
            new_password = st.text_input(
                "Choose Password",
                type="password"
            )
            confirm_password = st.text_input(
                "Confirm Password",
                type="password"
            )

            register_button = st.form_submit_button(
                "Register",
                use_container_width=True
            )

        if register_button:

            if (
                new_username.strip() == ""
                or new_password.strip() == ""
                or confirm_password.strip() == ""
            ):
                st.error("All fields are required.")

            elif new_password != confirm_password:
                st.error("Passwords do not match.")

            else:

                user = register_user(
                    new_username.strip(),
                    new_password
                )

                if user is None:
                    st.error("Username already exists.")
                else:
                    st.session_state["user_id"] = user["id"]
                    st.session_state["username"] = user["username"]

                    st.success("Registration successful!")
                    st.rerun()

    return False
