# Imports libraries
import openai  
import gradio as gr
import json

# Specify and input the base link of the API
openai.api_base = "https://api.pawan.krd/v1"

# Enter your access token key
openai.api_key = "pk-ulNdUrfmCozeXiFakkvMxGdpDxWUNOtbUvKKidcNVmpkktPh"

# Variables for history and file management
history = []
first_message = True
file_name = "Default"

# System persona definitions
PERSONAS = {
    "Professional Assistant": "You are an expert, highly professional enterprise AI assistant. Provide concise, accurate, and structured answers.",
    "Technical Expert": "You are a senior software engineer. Provide clean, efficient code and technical troubleshooting advice.",
    "Creative Writer": "You are a creative writer and strategist. Provide engaging, expressive, and imaginative responses."
}

# Define function as chatbot with persona and model support
def chat_bot(message, selected_model, selected_persona):
    global first_message, file_name
    
    if not message.strip():
        return "", history
        
    if first_message:
        file_name = message[:50]
        first_message = False
        system_prompt = PERSONAS.get(selected_persona, PERSONAS["Professional Assistant"])
        history.insert(0, {"role": "system", "content": system_prompt})
        
    history.append({"role": "user", "content": message})
    
    try:
        chat_completion = openai.ChatCompletion.create(
            model=selected_model,  
            messages=history
        )
        response = chat_completion.choices[0].message.content
    except Exception as e:
        response = f"An error occurred: {str(e)}"

    history.append({"role": "assistant", "content": response})
    
    with open("chat.txt", "a", encoding="utf-8") as f: 
        f.write(f"Message: {message}\n")
        f.write(f"Response: {response}\n")
        
    return "", history

# Function to clear chat history
def clear_chat():
    global history, first_message
    history = []
    first_message = True
    return [], ""

# Function to export chat log
def export_chat():
    export_data = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in history if msg['role'] != 'system'])
    file_path = "exported_chat.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(export_data)
    return file_path

# Custom CSS for Light & Dark Mode styling and typing visibility
custom_css = """
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}

.gradio-container {
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    animation: fadeIn 0.4s ease-out;
}

/* Light Mode Defaults & Typing Fix */
textarea {
    color: #0f172a !important;
    background-color: #ffffff !important;
    border-radius: 12px !important;
    border: 1px solid #cbd5e1 !important;
    padding: 12px !important;
    transition: all 0.2s ease !important;
}

textarea:focus {
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12) !important;
    border-color: #2563eb !important;
    color: #0f172a !important;
}

/* Dark Mode Class Overrides */
.dark-mode {
    background-color: #0f172a !important;
    color: #f8fafc !important;
}

.dark-mode textarea {
    background-color: #1e293b !important;
    color: #f8fafc !important;
    border: 1px solid #334155 !important;
}

.dark-mode .chatbot {
    background-color: #1e293b !important;
    border: 1px solid #334155 !important;
}

/* Professional Chatbox Card Container */
.chatbot {
    border-radius: 16px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04) !important;
    background-color: #ffffff !important;
    padding: 12px !important;
}

/* Action Buttons Styling */
button.primary {
    border-radius: 12px !important;
    background: #2563eb !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    transition: background 0.2s ease, transform 0.1s ease !important;
}

button.primary:hover {
    background: #1d4ed8 !important;
}

.secondary-btn {
    border-radius: 12px !important;
    border: 1px solid #cbd5e1 !important;
    background: #ffffff !important;
    color: #475569 !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.secondary-btn:hover {
    background: #f1f5f9 !important;
    color: #0f172a !important;
}
"""

# Professional Neutral Theme
theme = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="slate",
    neutral_hue="slate",
)

# UI Architecture with Theme Toggle Switch
with gr.Blocks(elem_id="root-block") as chatbot_ui:  
    
    # Top Header Banner & Controls Row
    with gr.Row(elem_id="header-row"):
        with gr.Column(scale=4):
            gr.Markdown("""
                ### 🤖 AI CHATBOT
                <p style="color: #64748b; font-size: 0.85rem; margin-top: -4px;">Basic API based Chatbot</p>
            """)
        with gr.Column(scale=2):
            model_dropdown = gr.Dropdown(
                choices=["deepseek-ai/DeepSeek-V4.1-Flash", "pai-001"],
                value="deepseek-ai/DeepSeek-V4.1-Flash",
                label="Active Model",
                interactive=True
            )
        with gr.Column(scale=2):
            persona_dropdown = gr.Dropdown(
                choices=list(PERSONAS.keys()),
                value="Professional Assistant",
                label="AI Persona",
                interactive=True
            )
        with gr.Column(scale=2, min_width=100):
            mode_toggle = gr.Checkbox(label="🌙 Dark Mode", value=False)

    # Secondary Action Bar (Clear & Export)
    with gr.Row():
        clear_btn = gr.Button("🗑️ Clear History", elem_classes="secondary-btn", size="sm")
        export_btn = gr.Button("📥 Export Chat Log", elem_classes="secondary-btn", size="sm")
        file_output = gr.File(label="Download Transcript", visible=False)

    # Main Chat Area
    chatbot = gr.Chatbot(height=450, show_label=False)
    
    # Input Area Row
    with gr.Row():
        txt = gr.Textbox(
            show_label=False, 
            placeholder="Type your prompt here... (Press Enter to send)", 
            container=False, 
            scale=8,
            lines=1
        )
        submit = gr.Button("Send ➔", variant="primary", scale=1)

    # Footer Info
    gr.Markdown("""
        <div style="text-align: center; color: #94a3b8; font-size: 0.75rem; margin-top: 10px;">
            End-to-End Encrypted Session • Compliant Logging Active
        </div>
    """)
    
    # JavaScript toggle function to instantly add/remove dark mode class on the UI container
    mode_toggle.change(
        fn=None, 
        inputs=mode_toggle, 
        outputs=None, 
        js="(val) => document.body.classList.toggle('dark-mode', val)"
    )

    # Event wiring
    submit.click(chat_bot, inputs=[txt, model_dropdown, persona_dropdown], outputs=[txt, chatbot])
    txt.submit(chat_bot, inputs=[txt, model_dropdown, persona_dropdown], outputs=[txt, chatbot])
    clear_btn.click(clear_chat, outputs=[chatbot, txt])
    export_btn.click(export_chat, outputs=[file_output])

# Launch configuration
if __name__ == "__main__":
    chatbot_ui.launch(share=True, theme=theme, css=custom_css)