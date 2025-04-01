from django import forms

from .models import Currency


class CurrencyConvertForm(forms.Form):
    amount = forms.DecimalField(label="Сумма", min_value=0.01, decimal_places=2)
    from_currency = forms.ModelChoiceField(
        queryset=Currency.objects.all(), label="Из валюты"
    )
    to_currency = forms.ModelChoiceField(
        queryset=Currency.objects.all(), label="В валюту"
    )
