import os
import sys
import asyncio
from pathlib import Path
from openai import AsyncOpenAI

async def main(prompt_file: Path):
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    system_prompt = prompt_file.read_text()

    # start with system prompt
    history = [{"role": "system", "content": system_prompt}]

    print("👋 Hi! I’m ScamDetector. Type 'quit' to exit.\n")

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
