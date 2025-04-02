from django import forms
from .models import Currency

class ConverterForm(forms.Form):
    amount = forms.DecimalField(
        label="Сумма",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "form-control form-control-lg rounded-3 border border-secondary-subtle shadow-sm",
            "placeholder": "Например: 10000"
        })
    )

    from_currency = forms.ModelChoiceField(
        queryset=Currency.objects.all(),
        label="Из валюты",
        widget=forms.Select(attrs={
            "class": "form-select form-select-lg rounded-3 border border-secondary-subtle shadow-sm"
        })
    )

    to_currency = forms.ModelChoiceField(
        queryset=Currency.objects.all(),
        label="В валюту",
        widget=forms.Select(attrs={
            "class": "form-select form-select-lg rounded-3 border border-secondary-subtle shadow-sm"
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        from_currency = cleaned_data.get("from_currency")
        to_currency = cleaned_data.get("to_currency")

        if from_currency and to_currency:
            if from_currency.code != "KZT" and to_currency.code != "KZT":
                raise forms.ValidationError(
                    "Одна из валют должна быть тенге (KZT - Тенге)."
                )