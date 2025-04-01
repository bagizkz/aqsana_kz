from datetime import date
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import CurrencyConvertForm
from .models import ExchangeRate, ConversionHistory
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

        if request.user.is_authenticated and isinstance(result, (int, float, Decimal)):
            print(f"Т Сохранение: {amount} {from_currency} → {to_currency} = {result}")
            ConversionHistory.objects.create(
                user=request.user,
                amount=Decimal(str(amount)),
                from_currency=from_currency,
                to_currency=to_currency,
                converted_amount=Decimal(str(result)),
            )

    return render(request, "convert.html", {
        "form": form,
        "result": result,
    })


@login_required
def conversion_history(request):
    history = ConversionHistory.objects.filter(user=request.user).order_by("-timestamp")
    return render(request, "conversion_history.html", {"history": history})