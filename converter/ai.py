import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_forecast(prompt: str) -> list:
    print("\n--- PROMPT GPT ---")
    print(prompt)
    print("------------------\n")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=200,
        temperature=0.3,
    )

    content = response.choices[0].message.content.strip()

    # извлечь JSON
    try:
        start = content.find('[')
        end = content.rfind(']') + 1
        json_str = content[start:end]
        parsed = json.loads(json_str)
        return parsed
    except Exception as e:
        print("Ошибка при разборе JSON от GPT:", e)
        return []
