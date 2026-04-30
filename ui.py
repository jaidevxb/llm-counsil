import streamlit as st
from council_logic import LLCouncil

# Initialize the Council Engine
council = LLCouncil()

st.set_page_config(page_title="Pro Council", layout="wide")
st.title("🏛️ Professional AI Council")

# Persistent memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar for model selection
with st.sidebar:
    st.header("Configuration")
    experts = st.multiselect(
        "Select Experts",
        ["groq/llama-3.3-70b-versatile", "gemini/gemini-3.1-pro", "groq/qwen/qwen3-32b"],
        default=["groq/llama-3.3-70b-versatile", "gemini/gemini-3.1-pro"]
    )

# Chat Input
if prompt := st.chat_input("Enter your query..."):
    # 1. Get Opinions & Synthesize
    with st.spinner("Experts are debating..."):
        drafts = council.get_expert_opinions(prompt, experts)
        report = council.synthesize(prompt, drafts)
    
    # 2. Save to history
    st.session_state.chat_history.append({"q": prompt, "a": report})

# Display the conversation
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["q"])
    with st.chat_message("assistant"):
        st.markdown(chat["a"])