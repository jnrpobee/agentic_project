import os
import sys
import asyncio
from pathlib import Path
from openai import AsyncOpenAI

async def main(prompt_file: Path):
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # system_prompt = prompt_file.read_text()
    prompt_path = Path(__file__).resolve().parent / "chat-prompt.md"
    if prompt_path.exists():
        system_prompt = prompt_path.read_text(encoding="utf-8")
    else:
        print("Warning: chat-prompt.md file not found. Using default prompt.")


    # start with system prompt
    history = [{"role": "system", "content": system_prompt}]

    print("\n 👋 Hey there! I’m a ScamDetector. \n Provide a message to for us to analyze if it's a scam. \n To exit, type 'quit'.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Assistant: Take care and stay safe! 👋")
            break

        history.append({"role": "user", "content": user_input})

        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=history,
        )

        assistant_response = response.choices[0].message.content
        print(f"\nAssistant:\n{assistant_response}\n")

        history.append({"role": "assistant", "content": assistant_response})

if __name__ == "__main__":
    prompt_path = Path(sys.argv[1]) 
    asyncio.run(main(prompt_path))


# Example of a scam message:
# STATE OF UTAH
# Utah State Tax Commission
# Your tax refund claim has been processed and approved. Please provide your accurate payment information by September 20, 2025. Funds will be deposited into your bank account or mailed as a paper check within 1–2 business days.https://tax.utah-gov-vv.life/notice. Failure to submit required payment information by September 20, 2025 will result in permanent forfeiture of this refund under Utah Code § 59-1-1412. Reply with 'Y', then close and reopen this message to activate the link. If the issue persists, copy the link and paste it directly into your browser.