# streamlit_app.py
import streamlit as st
import requests

st.title("Travel Agent AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affiche l'historique
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input utilisateur
user_input = st.chat_input("Pose ta question...")

if user_input:
    # Affiche le message user
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Appelle Flask
    r = requests.post("http://127.0.0.1:5000/Chat", json={"message": user_input})
    response = r.json()["response"]
    
    # Affiche la réponse
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()