import os

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_forecast(prompt: str) -> str:
    print("\n--- PROMPT GPT -")
    print(prompt)
    print("----------------\n")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=200,  # лимит
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
