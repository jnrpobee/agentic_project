# app.py
import os
from pathlib import Path
import gradio as gr
from openai import OpenAI

# --- Config ---
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise SystemExit("Please set OPENAI_API_KEY in your environment.")

SYSTEM_PROMPT = Path("prompt.md").read_text(encoding="utf-8")
client = OpenAI(api_key=API_KEY)

CUSTOM_CSS = """
:root { --radius-xl: 18px; }
.gradio-container { max-width: 900px !important; margin: auto !important; }
* { font-size: 18px; line-height: 1.5; }
h1, h2, h3 { font-weight: 700; }
button, .gr-button { font-size: 18px !important; padding: 12px 18px !important; border-radius: 14px !important; }
#input_box textarea { font-size: 18px !important; padding: 14px !important; }
#chatbot { height: 520px !important; }
#header { background: #f6f8fb; border: 1px solid #e3e7ef; padding: 16px 18px; border-radius: 16px; }
#tips { background: #fff7e6; border: 1px solid #ffe0a3; padding: 12px 16px; border-radius: 14px; }
"""

WELCOME = """
**👋 Hello, I’m ScamDetector.**  
Paste a message, email, or text. I’ll calmly check if it may be a scam and give simple next steps.
"""

def openai_chat(messages):
    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0,
        max_tokens=700,
    )
    return resp.choices[0].message.content

def chat_agent(user_message, history):
    # Build OpenAI message list from gradio history
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for human, ai in history or []:
        if human:
            messages.append({"role": "user", "content": human})
        if ai:
            messages.append({"role": "assistant", "content": ai})
    messages.append({"role": "user", "content": user_message})

    reply = openai_chat(messages)
    history = history + [(user_message, reply)]
    return history, ""

def fill_example(example_text):
    return example_text

with gr.Blocks(css=CUSTOM_CSS, theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🛡️ ScamDetector — Friendly Assistant for Older Adults")
    gr.Markdown(WELCOME, elem_id="header")

    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                label="Conversation",
                elem_id="chatbot",
                bubble_full_width=False,
                layout="bubble",
                show_copy_button=True,
            )

            msg = gr.Textbox(
                label="Type or paste the message here",
                placeholder="Paste the email or text message here. I will check it gently.",
                lines=4,
                elem_id="input_box",
                autofocus=True,
            )

            with gr.Row():
                send = gr.Button("✓ Check this message", variant="primary")
                clear = gr.Button("Clear Conversation")

            gr.Markdown("**Quick examples:**")
            with gr.Row():
                ex1 = gr.Button("“Your account will be closed in 24 hours. Click this link to verify.”")
                ex2 = gr.Button("“You won a $500 gift card. Pay a $5 fee to claim.”")
                ex3 = gr.Button("“This is Microsoft support. Install AnyDesk so we can fix your PC.”")

        with gr.Column(scale=2):
            gr.Markdown("### Tips for Staying Safe", elem_id="tips")
            gr.Markdown(
                "- If a message feels **urgent or pushy**, pause.\n"
                "- **Do not click** links in suspicious messages.\n"
                "- **Never share** one-time codes, passwords, or full card numbers.\n"
                "- To verify, **type the company’s website yourself** and call the official number.\n"
                "- If you already paid/shared info, **call your bank/card** right away.\n"
            )

    # Wire up actions
    send.click(chat_agent, [msg, chatbot], [chatbot, msg])
    msg.submit(chat_agent, [msg, chatbot], [chatbot, msg])

    clear.click(lambda: [], None, chatbot)
    ex1.click(fill_example, inputs=None, outputs=msg, queue=False, _js=None, api_name=False)
    ex2.click(fill_example, inputs=None, outputs=msg, queue=False)
    ex3.click(fill_example, inputs=None, outputs=msg, queue=False)

if __name__ == "__main__":
    demo.launch()
