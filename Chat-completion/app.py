import os
from pathlib import Path
import gradio as gr
import openai as OpenAI
from openai import OpenAI

# --- Setup ---
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# SYSTEM_PROMPT = Path("prompt.md").read_text()
prompt_path = Path(__file__).resolve().parent / "prompt.md"
if prompt_path.exists():
    SYSTEM_PROMPT = prompt_path.read_text(encoding="utf-8")
else:
    print("Warning: prompt.md file not found. Using default prompt.")

# --- Chat logic ---
def chat_with_agent(message, history):
    # Convert Gradio history (list of tuples) into OpenAI messages
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for human, ai in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": ai})
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or "gpt-4o"
        messages=messages,
        temperature=0
    )
    reply = response.choices[0].message.content
    return reply

# --- Gradio interface ---
chatbot = gr.ChatInterface(
    fn=chat_with_agent,
    title="🛡️ ScamDetector",
    description="A calm, friendly assistant to help older adults identify potential scams.",
    theme="soft",
    # retry_btn=None,
    # clear_btn="Clear Conversation"
)

if __name__ == "__main__":
    chatbot.launch()
