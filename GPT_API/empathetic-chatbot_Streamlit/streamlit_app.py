import streamlit as st
import requests

# Inject custom CSS for styling
st.markdown(
    """
    <style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f0f0f0;
        margin: 0;
        padding: 0;
    }
    .sidebar {
        background-color: #2f2f2f;
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-right: 20px;
    }
    .sidebar-button {
        background-image: linear-gradient(to right, #FF1493, #FF4500);
        border: none;
        border-radius: 20px;
        padding: 10px 20px;
        font-size: 16px;
        margin-top: 10px;
        cursor: pointer;
        color: white;
    }
    .sidebar-button:hover {
        filter: brightness(110%);
    }
    .sidebar-button:active {
        transform: translateY(1px);
    }
    .chat-container {
        background-color: #00;
        border-radius: 10px;
        padding: 5px;
    }
    .chat-message {
        margin-bottom: 6px;
    }
    .chat-history {
        margin-top: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to send message and retrieve bot's response
def send_message(message):
    response = requests.post('http://localhost:5000/chat', json={'message': message})
    bot_reply = response.json().get('reply', '')
    return bot_reply

# Main Streamlit UI
st.title("Empathetic Chatbot")

# Function to clear chat history
def clear_chat_history():
    st.session_state.chat_history = []



chat_history = st.empty()

user_input = st.text_area("Your message:")
if st.button("Submit 🔼"):
    if user_input.strip() != "":
        bot_reply = send_message(user_input)
        st.session_state.chat_history.append((user_input, bot_reply))

# Button to clear chat history
if st.button("Delete Chat 🗑️"):
    clear_chat_history()


# Initialize chat history in session state if not exists
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for user_msg, bot_reply in st.session_state.chat_history:
    st.markdown(f'<div class="chat-container"><p class="chat-message"><strong>👤:</strong> {user_msg}</p><p class="chat-message"><strong>🤖:</strong> {bot_reply}</p></div>', unsafe_allow_html=True)
    st.markdown('<hr class="chat-history">', unsafe_allow_html=True)
