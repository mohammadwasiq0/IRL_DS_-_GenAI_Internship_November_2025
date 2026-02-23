import streamlit as st
from auth.auth_handler import authenticate_user, register_user
from services.chat_service import process_chat
from memory.memory_manager import get_chat_history
import pandas as pd

st.set_page_config(page_title="Career Advisor Chatbot")

if "user" not in st.session_state:
    st.session_state.user = None

st.title("🎓 Career Advisor AI")

# Authentication
if not st.session_state.user:
    choice = st.radio("Login/Register", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button(choice):
        if choice == "Register":
            register_user(username, password)
            st.success("Registered successfully!")
        else:
            user = authenticate_user(username, password)
            if user:
                st.session_state.user = user
                st.success("Logged in!")
            else:
                st.error("Invalid credentials")

else:
    user_id = st.session_state.user.id

    user_input = st.chat_input("Ask your career question...")

    if user_input:
        response = process_chat(user_id, user_input)
        st.chat_message("user").write(user_input)
        st.chat_message("assistant").write(response)

    # Display History
    st.subheader("Chat History")
    history = get_chat_history(user_id)
    for chat in history:
        st.write(f"{chat.role}: {chat.message}")

    # Download history
    if st.button("Download Chat History"):
        data = [{"role": c.role, "message": c.message} for c in history]
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False)
        st.download_button("Download CSV", csv, "chat_history.csv")
