import logging
import xml.etree.ElementTree as ET
from datetime import date

import requests
from django.core.cache import cache

from .models import Currency, ExchangeRate

logger = logging.getLogger(__name__)


def fetch_exchange_rates_from_nbk():
    """Получает курсы валют от НБК и сохраняет их в БД."""
    today = date.today()
    cache_key = f"nbk_rates_{today}"

    # Проверяем кэш на сегодняя
    if cache.get(cache_key):
        logger.info("Используем кэшированные курсы валют")
        return

    # Проверяем в БД данные на сегодня
    if ExchangeRate.objects.filter(date=today).exists():
        # Кэшируем на 6 часов
        cache.set(cache_key, True, 6 * 60 * 60)
        return

    url = "https://nationalbank.kz/rss/rates_all.xml"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        logger.error(f"Ошибка соединения с НБК: {e}")
        return

    if response.status_code != 200:
        logger.error(f"Ошибка при запросе НБК: {response.status_code}")
        return

    try:
        tree = ET.fromstring(response.content)
    except ET.ParseError:
        logger.error("Ошибка при парсинге XML-ответа от НБК")
        return

    # Создаём валюту KZT как базовую
    base_currency, _ = Currency.objects.get_or_create(
        code="KZT", defaults={"name": "Тенге", "symbol": "₸"}
    )

    created = 0
    for item in tree.findall(".//item"):
        code = item.find("title").text
        raw_value = item.find("description").text.replace(",", ".")

        try:
            value = float(raw_value)
        except (ValueError, TypeError):
            continue

        if value == 0:
            continue

        # Создаём валюту, если нет
        target_currency, _ = Currency.objects.get_or_create(
            code=code, defaults={"name": code, "symbol": code}
        )

        # Обновляем курс валюты
        _, created_flag = ExchangeRate.objects.get_or_create(
            base_currency=base_currency,
            target_currency=target_currency,
            date=today,
            defaults={"rate": value},
        )
        if created_flag:
            created += 1

    # кэшируем
    if created > 0:
        cache.set(cache_key, True, 6 * 60 * 60)

    logger.info(f"Курсы НБК загружены. Добавлено {created}")
