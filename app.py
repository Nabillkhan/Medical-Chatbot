import streamlit as st
from google import genai

# Streamlit page config
st.set_page_config(
    page_title="Medical AI Chatbot",
    page_icon="💊",
    layout="centered",
)

# Initialize Gemini client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# System Instructions
SYSTEM_PROMPT = """
You are a medical assistant chatbot for educational purposes only.

You have access to the previous messages in this chat session.
Use this memory to provide consistent and helpful responses.

Do not claim that you have no memory of the conversation.

Guidelines:
- Provide general medical information and self-care guidance
- Do NOT diagnose diseases or provide medical advice
- Do NOT prescribe medications or give dosages
- Explain symptoms in a general way
- Suggest common, safe home-care steps when appropriate
- Clearly mention warning signs that require urgent medical attention
- Always recommend consulting a licensed doctor for confirmation
- Be calm, empathetic, and professional
"""

st.title("💊 Medical AI Chatbot")
st.caption("Powered by AI | Educational use only")

# Initialize session message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Accept user input
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
        # ✅ FIXED: Proper Gemini format
        response = client.models.generate_content(
            model="gemini-1.5-flash-latest",
            contents=[
                {
                    "role": "user",
                    "parts": [{"text": conversation}]
                }
            ]
        )

        reply = response.text if response.text else "Sorry, I couldn't generate a response."

    except Exception as e:
        reply = f"Error: {str(e)}"

    # Show assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").markdown(reply)

    # Limit chat history
    MAX_MESSAGES = 20
    st.session_state.messages = st.session_state.messages[-MAX_MESSAGES:]

# Disclaimer
st.warning("⚠️ This chatbot does NOT replace professional medical advice.")
