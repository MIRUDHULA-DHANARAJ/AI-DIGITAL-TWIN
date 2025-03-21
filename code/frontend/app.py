import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"
EVENTS_URL = "http://127.0.0.1:8000/events"

st.title("AI-Twin Chatbot 💬")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask AI-Twin..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = requests.post(API_URL, json={"message": user_input})
        response.raise_for_status()
        bot_response = response.json().get("response", "No response from AI.")
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")

# Fetch calendar events
st.subheader("Upcoming Events")
try:
    events_response = requests.get(EVENTS_URL)
    events_response.raise_for_status()
    events = events_response.json()
    for event in events:
        st.markdown(f"**{event['title']}** - {event['date']}")
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching events: {e}")
