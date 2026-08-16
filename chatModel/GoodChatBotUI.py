import streamlit as st
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
)

# =========================================================
# CONFIG
# =========================================================

load_dotenv()

st.set_page_config(
    page_title="Mistral Assistant",
    page_icon="🤖",
    layout="centered",
)

# =========================================================
# MODEL
# =========================================================

model = ChatMistralAI(
    model="mistral-small-2603"
)

# =========================================================
# SESSION STATE
# =========================================================

# Centralized system prompts (single source of truth)
prompts = {
    "Funny": "You are a very funny AI agent. You respond with humor and jokes.",
    "Angry": "You are an angry AI agent. You respond aggressively and impatiently.",
    "Sad": "You are a very sad AI agent. You respond in a depressed and emotional tone.",
}

def set_system(mod: str):
    """Set the system prompt and reset history to contain only the SystemMessage.

    Keeps a single place where the SystemMessage content is created.
    """
    st.session_state.mod = mod
    st.session_state.system_prompt = prompts.get(mod, prompts["Funny"])
    st.session_state.history = [SystemMessage(content=st.session_state.system_prompt)]


# Initialize session state with default system prompt if needed
if "mod" not in st.session_state and "history" not in st.session_state:
    set_system("Funny")
else:
    # Ensure history exists and the first message is the system prompt
    if "history" not in st.session_state:
        st.session_state.history = [SystemMessage(content=st.session_state.get("system_prompt", prompts["Funny"]))]
    if "mod" not in st.session_state:
        st.session_state.mod = "Funny"
    if "system_prompt" not in st.session_state:
        st.session_state.system_prompt = prompts.get(st.session_state.mod, prompts["Funny"])

# =========================================================
# CSS
# =========================================================

st.markdown(
    """
<style>

.stApp {
    background-color: #0f1117;
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 6rem;
}


/* ================================
   HEADER
================================ */

.app-header {
    text-align: center;
    padding: 15px 0 30px 0;
}

.app-icon {
    font-size: 42px;
    margin-bottom: 8px;
}

.app-title {
    font-size: 30px;
    font-weight: 700;
    color: #ffffff;
}

.app-subtitle {
    margin-top: 6px;
    font-size: 14px;
    color: #8b93a7;
}


/* ================================
   CHAT
================================ */

div[data-testid="stChatMessage"] {
    background: transparent;
    padding: 8px 0;
}


/* Assistant */

div[data-testid="stChatMessage"]:has(
    div[data-testid="chatAvatarIcon-assistant"]
) {
    background-color: #1a1e27;
    border: 1px solid #292f3b;
    border-radius: 18px;
    padding: 14px 18px;
    margin: 12px 0;
}


/* User */

div[data-testid="stChatMessage"]:has(
    div[data-testid="chatAvatarIcon-user"]
) {
    background-color: #2563eb;
    border-radius: 18px;
    padding: 12px 18px;
    margin: 12px 0 12px auto;
    max-width: 75%;
}


/* Message text */

div[data-testid="stChatMessage"] p {
    color: #ffffff;
    font-size: 15px;
    line-height: 1.6;
}


/* ================================
   CHAT INPUT
================================ */

/* Remove outer border */

div[data-testid="stChatInput"] {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    background: transparent !important;
}


/* Remove wrapper border */

div[data-testid="stChatInput"] > div {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    background: transparent !important;
}


/* Input itself */

div[data-testid="stChatInput"] textarea {
    background-color: #1b1f28 !important;
    color: #ffffff !important;

    border: 1px solid #303744 !important;
    border-radius: 18px !important;

    padding: 14px 55px 14px 17px !important;

    font-size: 15px !important;

    outline: none !important;
    box-shadow: none !important;
}


/* Focus */

div[data-testid="stChatInput"] textarea:focus {
    border: 2px solid #4f7cff !important;
    outline: none !important;
    box-shadow: none !important;
}


/* Parent when focused */

div[data-testid="stChatInput"]:focus-within {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}


/* Send button */

div[data-testid="stChatInput"] button {
    background-color: #303541 !important;
    border: none !important;
    border-radius: 10px !important;
}


/* ================================
   CLEAR BUTTON
================================ */

.stButton button {
    background-color: transparent !important;
    color: #ffffff !important;

    border: 1px solid #353b48 !important;
    border-radius: 10px !important;

    height: 44px;
}

.stButton button:hover {
    border-color: #4f7cff !important;
    background-color: #181c25 !important;
}


/* ================================
   HIDE STREAMLIT UI
================================ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# HEADER
# =========================================================

# IMPORTANT:
# No HTML here. Using native Streamlit markdown.

st.markdown(
    """
<div style="text-align:center; padding:15px 0 30px 0;">
<div style="font-size:42px;">🤖</div>
<div style="font-size:30px; font-weight:700; color:white;">
Mistral Assistant
</div>
<div style="font-size:14px; color:#8b93a7; margin-top:6px;">
Your funny AI companion powered by Mistral
</div>
</div>
""",
    unsafe_allow_html=True,
)

# =========================================================
# DISPLAY CHAT
# =========================================================

# Sidebar controls for assistant tone
with st.sidebar:
    st.header("Settings")
    options = ["Funny", "Angry", "Sad"]
    default_index = options.index(st.session_state.get("mod", "Funny"))
    tone = st.selectbox("Assistant Tone", options, index=default_index)
    if st.button("Apply tone"):
        set_system(tone)
        st.rerun()

# Render chat messages (skip the SystemMessage which contains system prompt)
for message in st.session_state.history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user", avatar="👤"):
            st.write(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant", avatar="🤖"):
            st.write(message.content)

# Clear conversation button (only if there are user/AI messages)
non_system_msgs = [m for m in st.session_state.history if not isinstance(m, SystemMessage)]
if len(non_system_msgs) > 0:
    if st.button("🗑️ Clear conversation", use_container_width=True):
        # Reset to the current mode's system prompt
        set_system(st.session_state.get("mod", "Funny"))
        st.rerun()

# =========================================================
# INPUT
# =========================================================

text = st.chat_input("Message Mistral...")

# =========================================================
# PROCESS MESSAGE
# =========================================================

if text:
    # Exit command
    if text.strip().lower() == "exit":
        st.session_state.history.append(HumanMessage(content=text))
        st.session_state.history.append(AIMessage(content="See you later..! 👋"))
        st.rerun()

    # Add user message
    st.session_state.history.append(HumanMessage(content=text))

    # Prepare mode and messages (single place for SystemMessage content)
    mode = st.session_state.get("mod", "Funny")
    system_msg = st.session_state.get("system_prompt", prompts[mode])
    messages = st.session_state.history

    # Get response from model
    with st.spinner("Mistral is thinking... 🤔"):
        result = model.invoke(messages)

    # Append AI response and refresh
    st.session_state.history.append(AIMessage(content=result.content))
    st.rerun()