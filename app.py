import streamlit as st
from google import genai

# Page config
st.set_page_config(
    page_title="Medical AI Chatbot",
    page_icon="💊",
    layout="centered",
)

# Initialize Gemini client (API key from secrets)
client = genai.Client(api_key="AIzaSyDDc86iq3NcoXT-CEr8BU6fHc5sZmg2REg")

# System Prompt
SYSTEM_PROMPT = """
You are a medical assistant chatbot for educational purposes only.

You have access to previous chat messages.
Use them to provide helpful and consistent responses.

Guidelines:
- Provide general medical information only
- Do NOT diagnose or prescribe
- Suggest safe home-care tips
- Mention warning signs
- Always recommend consulting a doctor
- Be calm and professional
"""

# UI
st.title("💊 Medical AI Chatbot")
st.caption("Educational use only")

# Session memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask a medical question...")

if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    # Build conversation string
    conversation = SYSTEM_PROMPT + "\n"

    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        conversation += f"{role.capitalize()}: {content}\n"

    try:
        # ✅ Correct Gemini request
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                {
                    "role": "user",
                    "parts": [{"text": conversation}]
                }
            ]
        )

        # Extract response safely
        reply = response.text if response.text else "Sorry, I couldn't understand that."

    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    # Show assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").markdown(reply)

    # Limit memory
    MAX_MESSAGES = 20
    st.session_state.messages = st.session_state.messages[-MAX_MESSAGES:]

# Disclaimer
st.warning("⚠️ This chatbot does NOT replace professional medical advice.")
