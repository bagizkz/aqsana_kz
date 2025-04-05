import json
import logging
import os

from openai import OpenAI

logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_forecast(prompt: str) -> list:
    """
    Генерирует прогноз курса валют используя GPT-3.5-turbo.

    Args:
        prompt: Запрос для модели GPT

    Returns:
        list: Прогнозы в формате списка словарей
    """
    logger.debug("Отправка запроса к GPT API")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.3,
        )

        content = response.choices[0].message.content.strip()

        # Извлекаем JSON из ответа
        start = content.find("[")
        end = content.rfind("]") + 1

        if start == -1 or end == 0:
            logger.error("Не найден JSON в ответе GPT")
            return []

        json_str = content[start:end]

        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка при разборе JSON от GPT: {e}")
            return []

    except Exception as e:
        logger.error(f"Ошибка при запросе к OpenAI API: {e}")
        return []
