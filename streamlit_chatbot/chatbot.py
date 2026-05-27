import streamlit as st
import streamlit.components.v1 as components
from google import genai

# Configure Gemini
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(
    page_title="StudyBuddy Match", 
    page_icon="📚", 
    layout="wide")

# Load HTML app
with open("studybuddy.html", "r", encoding="utf-8") as f:
    html_data = f.read()

# Show HTML UI
components.html(html_data, height=900, scrolling=True)

st.divider()

# REAL Gemini chatbot
st.title("Real AI Study Tutor")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
prompt = st.chat_input("Ask your AI tutor...")

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        ai_reply = response.text

    except Exception as e:
        ai_reply = str(e)

    with st.chat_message("assistant"):
        st.write(ai_reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })