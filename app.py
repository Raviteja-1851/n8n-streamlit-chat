import streamlit as st
import requests
import os
import json

# ✅ Always load webhook URL from secrets (no hardcoded ngrok!)
N8N_WEBHOOK = st.secrets["N8N_WEBHOOK"]

st.set_page_config(page_title="n8n AI Agent Chat", page_icon="🤖")
st.title("🤖 Chat with n8n AI Agent")

# Keep chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Display history so far
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Save and display user message
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Assistant streaming reply
    with st.chat_message("assistant"):
        placeholder = st.empty()
        text_output = ""

        try:
            with requests.post(
                N8N_WEBHOOK,
                json={"text": user_input},
                stream=True,
                timeout=300
            ) as r:
                if r.status_code == 200:
                    for chunk in r.iter_content(chunk_size=None):
                        if chunk:
                            try:
                                event = json.loads(chunk.decode("utf-8"))
                                # ✅ Only display "item" events with content
                                if event.get("type") == "item" and "content" in event:
                                    text_output += event["content"]
                                    placeholder.write(text_output)
                            except json.JSONDecodeError:
                                # Ignore keep-alives or malformed bits
                                pass

                    # Save assistant reply to history after stream ends
                    st.session_state.history.append(
                        {"role": "assistant", "content": text_output}
                    )
                else:
                    placeholder.error(f"❌ n8n error: {r.status_code} - {r.text}")

        except Exception as e:
            placeholder.error(f"⚠️ Request failed: {e}")
