import xml.etree.ElementTree as ET
from datetime import date

import requests

from .models import Currency, ExchangeRate


def fetch_exchange_rates_from_nbk():
    url = "https://nationalbank.kz/rss/rates_all.xml"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Т Ошибка при запросе НБК: {response.status_code}")
        return

    tree = ET.fromstring(response.content)

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

        # Сохраняем курс KZT → target как есть
        _, created_flag = ExchangeRate.objects.get_or_create(
            base_currency=base_currency,
            target_currency=target_currency,
            date=date.today(),
            defaults={"rate": value},
        )
        if created_flag:
            created += 1
    print("----------------------\n")
    print(f"Т Курсы НБК загружены. Добавлено {created}")
    print("----------------------\n")
