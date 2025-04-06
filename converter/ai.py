import json
import logging
import os

from openai import OpenAI

logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_forecast(prompt: str) -> list:
    """Генерирует прогноз курса валют через GPT-3.5-turbo."""
    logger.info(f"🔶 PROMPT 🔶 {prompt}")

    try:
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.2,
        )
        content = resp.choices[0].message.content.strip()
        logger.info(f"🔷 RESPONSE 🔷 {content}")

        # Extract JSON
        start = content.find("[")
        end = content.rfind("]") + 1
        json_str = content[start:end] if start >= 0 and end > 0 else ""

        if not json_str:
            logger.error("❌ JSON не найден")
            return []

        result = json.loads(json_str)
        logger.info(f"✅ FORECAST ✅ {result}")
        return result

    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON ошибка: {e}")
        return []
    except Exception as e:
        logger.error(f"❌ API ошибка: {e}")
        return []
