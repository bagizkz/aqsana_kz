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
from .rates_service import fetch_exchange_rates_from_nbk


@require_http_methods(["GET", "POST"])
def convert_currency(request):
    result = None
    prediction = []

    # Обновляем курсы валют
    fetch_exchange_rates_from_nbk()

    # Настройка формы
    defaults = {"KZT": "USD"} if request.method == "GET" else None
    form = setup_form(request, defaults)

    # Обработка конвертации
    if request.method == "POST" and form.is_valid():
        result, prediction = process_conversion(request, form)

    # Получение избранных
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
        },
    )


def setup_form(request, defaults=None):
    """Настраивает форму конвертера."""
    if defaults:
        default_from = Currency.objects.filter(code="KZT").first()
        default_to = Currency.objects.filter(code="USD").first()
        return ConverterForm(
            initial={"from_currency": default_from, "to_currency": default_to}
        )
    return ConverterForm(request.POST)


def process_conversion(request, form):
    """Обрабатывает запрос на конвертацию валюты."""
    amount = form.cleaned_data["amount"]
    from_currency = form.cleaned_data["from_currency"]
    to_currency = form.cleaned_data["to_currency"]
    prediction = []

    # Конвертация
    if from_currency == to_currency:
        result = amount
    else:
        result = convert_amount(from_currency, to_currency, amount)

    # Сохранение в историю
    if request.user.is_authenticated and isinstance(result, (int, float, Decimal)):
        ConversionHistory.objects.create(
            user=request.user,
            amount=Decimal(str(amount)),
            from_currency=from_currency,
            to_currency=to_currency,
            converted_amount=Decimal(str(result)),
        )

    # Генерация прогноза
    if from_currency.code == "KZT" and to_currency.code == "USD":
        prediction = generate_rate_prediction(from_currency, to_currency)

    return result, prediction


def convert_amount(from_currency, to_currency, amount):
    """Конвертирует сумму из одной валюты в другую."""
    try:
        # Ищем прямой курс
        rate = ExchangeRate.objects.get(
            base_currency=from_currency,
            target_currency=to_currency,
            date=date.today(),
        ).rate

        is_kzt_base = from_currency.code == "KZT"
        return round(amount / rate if is_kzt_base else amount * rate, 2)

    except ExchangeRate.DoesNotExist:
        try:
            # Ищем обратный курс
            reverse_rate = ExchangeRate.objects.get(
                base_currency=to_currency,
                target_currency=from_currency,
                date=date.today(),
            ).rate

            is_kzt_target = to_currency.code == "KZT"
            return round(
                amount * reverse_rate if is_kzt_target else amount / reverse_rate, 2
            )

        except ExchangeRate.DoesNotExist:
            return "Бүгінге валюта бағамы жоқ"


def generate_rate_prediction(from_currency, to_currency):
    """Генерирует прогноз курса на неделю вперед."""
    qs = ExchangeRate.objects.filter(
        base_currency=from_currency,
        target_currency=to_currency,
    ).order_by("date")

    if qs.count() < 2:
        return []

    data = [(rate.date.strftime("%Y-%m-%d"), float(rate.rate)) for rate in qs]
    short_data = [f"{d}: {r}" for d, r in data[-7:]]

    prompt = (
        f"KZT-USD rates: {', '.join(short_data)}\n"
        "Predict next 7 days rates. Return only JSON: "
        '[{"date":"YYYY-MM-DD","rate":number}]'
    )

    return generate_forecast(prompt)


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
