import streamlit as st
import openai
import os

# === Set OpenAI API Key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
    st.error("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
    st.stop()

# CSS for dark black and blue theme
dark_blue_css = """
<style>
    body {
        background-color: #0a0e16;
        color: #c3d0e5;
    }
    .css-1d391kg {
        background-color: #121922;
        color: #a3b1cc;
    }
    .streamlit-expanderHeader {
        font-weight: bold;
        color: #1e90ff;
    }
    /* Sidebar styling */
    .css-1d391kg [data-testid="stSidebar"] {
        background-color: #0a0e16;
        color: #1e90ff;
    }
    /* Wide layout background */
    .css-18e3th9 {
        background-color: #0a0e16;
        color: #c3d0e5;
    }
    /* Chat container */
    .chat-container {
        border-radius: 10px;
        background-color: #121922;
        padding: 15px;
        min-height: 400px;
        max-height: 600px;
        overflow-y: auto;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .user-message {
        color: #1e90ff;
        margin-bottom: 0.75rem;
        font-weight: 600;
    }
    .bot-message {
        color: #99bbff;
        margin-bottom: 0.75rem;
        font-style: italic;
    }
    input, .stTextInput>div>input {
        background-color: #222a3a;
        color: #c3d0e5;
        border-color: #1e90ff;
    }
    button[kind="primary"] {
        background-color: #1e90ff;
        color: black;
        font-weight: bold;
    }
</style>
"""

st.set_page_config(page_title="Study AI Chatbot Dashboard", layout="wide")
st.markdown(dark_blue_css, unsafe_allow_html=True)

# Sidebar menu on left
with st.sidebar:
    st.title("📚 Study Dashboard")
    st.markdown("### Menu")
    menu_items = [
        "📅 Daily Planner",
        "🗓️ Weekly Planner",
        "📆 Monthly Planner",
        "🔄 Revision Planner",
        "💡 Flashcards",
        "👥 Study Groups",
        "📈 Progress Graphs",
        "⏳ Days Left for Exams",
        "😊 Mood Analyzer",
    ]
    for item in menu_items:
        st.markdown(f"- {item}")

    st.markdown("---")
    # Dark mode toggle dummy for UI
    dark_mode = st.checkbox("Enable Dark Mode", value=True, help="UI theme currently forced dark")

# Main content area for AI Chatbot
st.title("🤖 AI Study Chatbot")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# User input text box
user_input = st.text_input("Chat with your Study Assistant")

def ask_openai(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

if user_input:
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Query OpenAI API with full conversation history
    bot_response = ask_openai(st.session_state.chat_history)
    # Append bot response
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

# Chat history display container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f'<div class="user-message"><b>You:</b> {chat["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message"><b>Bot:</b> {chat["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
