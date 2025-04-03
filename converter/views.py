from datetime import date
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .ai import generate_forecast
from .forms import ConverterForm
from .models import (
    ConversionHistory,
    Currency,
    ExchangeRate,
    FavoriteConversionDirection,
)
from .utils import fetch_exchange_rates_from_nbk


@require_http_methods(["GET", "POST"])
def convert_currency(request):
    result = None
    prediction = []
    ai_forecast = ""

    fetch_exchange_rates_from_nbk()

    if request.method == "GET":
        default_from = Currency.objects.filter(code="KZT").first()
        default_to = Currency.objects.filter(code="USD").first()
        form = ConverterForm(
            initial={"from_currency": default_from, "to_currency": default_to}
        )
    else:
        form = ConverterForm(request.POST)

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
            ConversionHistory.objects.create(
                user=request.user,
                amount=Decimal(str(amount)),
                from_currency=from_currency,
                to_currency=to_currency,
                converted_amount=Decimal(str(result)),
            )







        if from_currency.code == "KZT" and to_currency.code == "USD":
            qs = ExchangeRate.objects.filter(
                base_currency=from_currency,
                target_currency=to_currency,
            ).order_by("date")

            if qs.count() >= 2:
                data = [
                    (rate.date.strftime("%Y-%m-%d"), float(rate.rate)) for rate in qs
                ]
                short_data = [f"{d}: {r}" for d, r in data[-7:]]

                prompt = (
                    f"На основе курса KZT к USD:\n"
                    + "\n".join(short_data)
                    + '\nДай прогноз курса на 7 дней вперёд. Верни только JSON в формате: [{"date": "YYYY-MM-DD", "rate": Число}]'
                )

                prediction = generate_forecast(prompt)

    favorites = (
        FavoriteConversionDirection.objects.filter(user=request.user)
        if request.user.is_authenticated
        else []
    )
    favorite_strings = [
        f"{f.from_currency.code}-{f.to_currency.code}" for f in favorites
    ]

    return render(
        request,
        "convert.html",
        {
            "form": form,
            "result": result,
            "favorites": favorites,
            "favorite_strings": favorite_strings,
            "prediction": prediction,
            "ai_forecast": ai_forecast,
        },
    )


@login_required
def conversion_history(request):
    history = ConversionHistory.objects.filter(user=request.user).order_by(
        "-created_at"
    )
    return render(request, "conversion_history.html", {"history": history})


@login_required
def add_to_favorites(request, from_code, to_code):
    from_currency = get_object_or_404(Currency, code=from_code)
    to_currency = get_object_or_404(Currency, code=to_code)
    FavoriteConversionDirection.objects.get_or_create(
        user=request.user, from_currency=from_currency, to_currency=to_currency
    )
    return redirect("convert")


@login_required
def remove_from_favorites(request, from_code, to_code):
    from_currency = get_object_or_404(Currency, code=from_code)
    to_currency = get_object_or_404(Currency, code=to_code)
    FavoriteConversionDirection.objects.filter(
        user=request.user, from_currency=from_currency, to_currency=to_currency
    ).delete()
    return redirect("convert")