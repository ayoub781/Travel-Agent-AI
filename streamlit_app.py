# streamlit_app.py
import streamlit as st
import requests

st.title("Travel Agent AI")
st.caption("Météo + Prix de vols en temps réel")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ex: Je veux aller à Tokyo depuis Paris du 15 jan au 15 fév 2027, quel temps fera t-il...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Recherche en cours... (peut prendre 2-3 min)"):
            r = requests.post(
                "http://127.0.0.1:5000/Chat",
                json={"message": user_input},
                timeout=600
            )
            response = r.json()["response"]
            tours = r.json()["tours"]
        
        st.markdown(response)
        st.caption(f"Tours de réflexion : {tours}")
    
    st.session_state.messages.append({"role": "assistant", "content": response})