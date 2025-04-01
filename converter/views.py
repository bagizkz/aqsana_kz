from datetime import date

from django.shortcuts import render

from .forms import CurrencyConvertForm
from .models import ExchangeRate
from .utils import fetch_exchange_rates_from_nbk


def convert_currency(request):
    result = None
    form = CurrencyConvertForm(request.POST or None)

    fetch_exchange_rates_from_nbk()

    if request.method == "POST" and form.is_valid():
        amount = form.cleaned_data["amount"]
        from_currency = form.cleaned_data["from_currency"]
        to_currency = form.cleaned_data["to_currency"]

        if from_currency == to_currency:
            result = amount
        else:
            try:
                rate = ExchangeRate.objects.get(
                    base_currency=from_currency,
                    target_currency=to_currency,
                    date=date.today(),
                ).rate

                if from_currency.code == "KZT":
                    result = round(amount / rate, 2)
                else:
                    result = round(amount * rate, 2)

            except ExchangeRate.DoesNotExist:
                try:
                    reverse_rate = ExchangeRate.objects.get(
                        base_currency=to_currency,
                        target_currency=from_currency,
                        date=date.today(),
                    ).rate

                    if to_currency.code == "KZT":
                        result = round(amount * reverse_rate, 2)
                    else:
                        result = round(amount / reverse_rate, 2)

                except ExchangeRate.DoesNotExist:
                    print(
                        f"Нет курса: {from_currency.code} → {to_currency.code} на {date.today()}"
                    )
                    result = "Курс не найден на сегодня"

    return render(request, "convert.html", {"form": form, "result": result})
