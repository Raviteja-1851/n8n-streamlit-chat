import streamlit as st
import requests
import os

# Load n8n webhook URL from Streamlit secrets or fallback
N8N_WEBHOOK = os.getenv("N8N_WEBHOOK", st.secrets.get("N8N_WEBHOOK", "https://caf1021b93c8.ngrok-free.app/webhook/chat-stream"))

st.set_page_config(page_title="n8n AI Agent Chat", page_icon="🤖")
st.title("🤖 Chat with n8n AI Agent")

# Store chat history in Streamlit session
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.chat_input("Ask me anything...")

if user_input:
    # Add user message
    st.session_state.history.append({"role": "user", "content": user_input})

    # Display conversation so far
    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Call n8n webhook
    with st.chat_message("assistant"):
        placeholder = st.empty()
        text_output = ""

        try:
            response = requests.post(N8N_WEBHOOK, json={"text": user_input}, timeout=60)

            if response.status_code == 200:
                try:
                    data = response.json()
                    text_output = data.get("text") or str(data)
                except:
                    text_output = response.text

                placeholder.write(text_output)
                st.session_state.history.append({"role": "assistant", "content": text_output})
            else:
                placeholder.error(f"Error from n8n: {response.status_code} - {response.text}")

        except Exception as e:
            placeholder.error(f"Request failed: {e}")
