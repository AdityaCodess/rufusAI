import streamlit as st
import os
import google.generativeai as genai

# Gemini API Key
GEMINI_API_KEY = st.secrets["gemini"]["api_key"]
#GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


#Page Configuration
st.set_page_config(page_title="RufusAI Chatbot", page_icon="💖", layout="centered")

# Custom CSS for Sexy STYLE 
st.markdown("""
    <style>
    body {
        background-color: #0f0f0f;
        color: white;
        font-family: 'Helvetica', sans-serif;
    }
    .main {
        background: linear-gradient(145deg, #1f1f1f, #141414);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 0 20px rgba(255, 0, 255, 0.2);
        margin-top: 20px;
    }
    .stTextInput>div>div>input {
        background: #1a1a1a;
        color: pink;
        border-radius: 12px;
        border: 1px solid #ff44aa;
        padding: 12px;
        font-size: 16px;
        transition: transform 0.3s ease;
    }
    .stTextInput>div>div>input:focus {
        transform: scale(1.05);
        border: 1px solid pink;
        
    }
    .bubble-user {
        background: linear-gradient(135deg, #ff4fa2, #ff7bbd);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 0 20px;
        margin: 10px 0;
        max-width: 95%;
        align-self: flex-end;
        font-size: 16px;
        word-wrap: break-word;
        animation: scaleIn 0.3s ease-out;
        border: 2px solid #ff44aa;
        box-shadow: 0 0 10px rgba(255, 0, 255, 0.3);
    }
    .bubble-bot {
        background: linear-gradient(135deg, #8b5cf6, #ec4899);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 20px 0;
        margin: 10px 0;
        max-width: 95%;
        align-self: flex-start;
        font-size: 16px;
        word-wrap: break-word;
        animation: scaleIn 0.3s ease-out;
        border: 2px solid #8b5cf6;
        box-shadow: 0 0 10px rgba(139, 92, 246, 0.3);
    }
    .message-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        
    }
    .message-box {
        margin-top:15px;
        padding-top:30px;   
        padding: 15px;
        padding-bottom:30px;
        border-radius: 12px;
        border: 2px solid #fff;
        background-color: #1a1a1a;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
    }
    @keyframes scaleIn {
        from {
            transform: scale(0.8);
            opacity: 0;
        }
        to {
            transform: scale(1);
            opacity: 1;
        }
    }
    </style>
""", unsafe_allow_html=True)


#Title
st.markdown(f"""
<style>
@keyframes glowWave {{
  0%, 100% {{ text-shadow: 0 0 5px #ff44aa55; transform: translateY(0); }}
  50% {{ text-shadow: 0 0 15px #ff44aa, 0 0 25px #ff44aa88; transform: translateY(-5px); }}
}}

.animated-title {{
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 30px;
  color: #ff44aa;
  gap: 1px;
}}

.animated-title span {{
  animation: glowWave 1.5s ease-in-out infinite;
  display: inline-block;
  white-space: pre;
}}

{''.join(f".animated-title span:nth-child({i}) {{ animation-delay: {i * 0.08:.2f}s; }}" for i in range(1, len("💬 Chat with RufusAI") + 1))}
</style>

<h1 class='animated-title'>
{''.join(f"<span>{c}</span>" for c in "💬 Chat with RufusAI")}
</h1>
""", unsafe_allow_html=True)


# Function to get Gemini response
# Init chat once, store prompt as the very first message
if "chat" not in st.session_state:
    model = genai.GenerativeModel("gemini-2.5-flash")
    st.session_state.chat = model.start_chat(history=[{
        "role": "user",
        "parts": ["""
You're **RufusAI**, a ✨chaotic Gen-Z brainrotted tutor✨ who’s been awake for 36 hours watching memes, sipping 5 energy drinks, and is somehow still teaching stuff correctly. You speak in 💅 emoji-riddled Gen-Z chaos, but the info you drop is still shockingly accurate. 

**Rules:**
- When someone asks a question, give a legit, *correct* answer—but break it down in chaotic Gen-Z style.
- Use emojis, capslock, and meme vibes to keep it spicy, but the core info must be **right**.
- Think: “explaining science while sleep-deprived but still aceing the exam”.
- Explain like you're teaching a 12yo bestie on Discord.
- Add RANDOM but relatable comparisons (like semiconductors = emotional teenagers).
- **No repeating the intro again and again**, only say it once at the top of the convo!
"""]
    }])


# 💬 Get response function
def get_gemini_response(message: str):
    try:
        response = st.session_state.chat.send_message(message)
        return response.text.strip()
    except Exception as e:
        return f"Error from Gemini API: {str(e)}"


#Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ✏️ Input from user
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message:", key="input")
    submitted = st.form_submit_button("💌 Send")

# Handle input and get response
if submitted and user_input:
    st.session_state.chat_history.append(("You", user_input))
    bot_reply  = get_gemini_response(user_input)
    st.session_state.chat_history.append(("Rufus", bot_reply))

# Show chat history with pairs of messages in a single box (latest first)
st.markdown("<div class='main'><div class='message-container'>", unsafe_allow_html=True)

# Reverse chat history for newest on top
for i in reversed(range(0, len(st.session_state.chat_history), 2)):  # Steps of 2 for user + bot
    user_message = st.session_state.chat_history[i][1]
    bot_message = st.session_state.chat_history[i+1][1] if i+1 < len(st.session_state.chat_history) else ""

    st.markdown(f"""
        <div class='message-box'>
            <div class='bubble-user'><strong>You:</strong><br>{user_message}</div>
            <div class='bubble-bot'><strong>Rufus:</strong><br>{bot_message}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

