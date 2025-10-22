import streamlit as st
import requests
import os

# ✅ Always load webhook URL from secrets
N8N_WEBHOOK = st.secrets["N8N_WEBHOOK"]

st.set_page_config(page_title="n8n AI Agent Chat", page_icon="🤖")
st.title("🤖 Chat with n8n AI Agent")

# Store chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Display past messages
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Save user msg
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Assistant reply (streaming placeholder)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        text_output = ""

        try:
            with requests.post(N8N_WEBHOOK, json={"text": user_input}, stream=True, timeout=300) as r:
                if r.status_code == 200:
                    for chunk in r.iter_content(chunk_size=None):
                        if chunk:
                            piece = chunk.decode("utf-8")
                            text_output += piece
                            placeholder.write(text_output)
                    st.session_state.history.append({"role": "assistant", "content": text_output})
                else:
                    placeholder.error(f"❌ n8n error: {r.status_code} - {r.text}")
        except Exception as e:
            placeholder.error(f"⚠️ Request failed: {e}")
