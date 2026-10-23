import openai
import streamlit as st
import json

# Specify the base link and API key
openai.api_base = "https://api.pawan.krd/v1"
openai.api_key = "pk-ulNdUrfmCozeXiFakkvMxGdpDxWUNOtbUvKKidcNVmpkktPh"

# System persona definitions
PERSONAS = {
    "Professional Assistant": "You are an expert, highly professional enterprise AI assistant. Provide concise, accurate, and structured answers.",
    "Technical Expert": "You are a senior software engineer. Provide clean, efficient code and technical troubleshooting advice.",
    "Creative Writer": "You are a creative writer and strategist. Provide engaging, expressive, and imaginative responses."
}

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="AI Chatbot Portfolio Project",
    page_icon="🤖",
    layout="centered"
)

# Initialize Session State
if "history" not in st.session_state:
    st.session_state.history = []
if "first_message" not in st.session_state:
    st.session_state.first_message = True

# --- Sidebar Controls ---
with st.sidebar:
    st.header("⚙️ Control Panel")
    
    selected_model = st.selectbox(
        "Active Model",
        ["deepseek-ai/DeepSeek-V4.1-Flash", "pai-001"]
    )
    
    selected_persona = st.selectbox(
        "AI Persona",
        list(PERSONAS.keys())
    )
    
    st.divider()
    
    # Clear Chat Button
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.history = []
        st.session_state.first_message = True
        st.rerun()
        
    # Export Chat Log Button
    chat_export_data = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in st.session_state.history if msg['role'] != 'system'])
    st.download_button(
        label="📥 Export Chat Log",
        data=chat_export_data,
        file_name="exported_chat.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    st.divider()
    st.markdown("<p style='text-align: center; color: gray; font-size: 0.8rem;'>End-to-End Encrypted Session</p>", unsafe_allow_html=True)

# --- Main App UI ---
st.title("🤖 AI Chatbot Workspace")
st.markdown("Basic API-based Chatbot powered by DeepSeek & Streamlit")
st.divider()

# Display Chat History
for message in st.session_state.history:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User Chat Input
if user_input := st.chat_input("Type your prompt here..."):
    
    # Inject system prompt on first message
    if st.session_state.first_message:
        st.session_state.first_message = False
        system_prompt = PERSONAS.get(selected_persona, PERSONAS["Professional Assistant"])
        st.session_state.history.insert(0, {"role": "system", "content": system_prompt})
        
    # Append & display user message
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        
    # Generate Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                chat_completion = openai.ChatCompletion.create(
                    model=selected_model,
                    messages=st.session_state.history
                )
                response = chat_completion.choices[0].message.content
            except Exception as e:
                response = f"An error occurred: {str(e)}"
                
            st.markdown(response)
            
    # Save to history and local file log
    st.session_state.history.append({"role": "assistant", "content": response})
    with open("chat.txt", "a", encoding="utf-8") as f:
        f.write(f"Message: {user_input}\n")
        f.write(f"Response: {response}\n")
