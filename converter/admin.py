from django.contrib import admin

from .models import Currency, ExchangeRate


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "symbol")
    search_fields = ("code", "name")


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ("base_currency", "target_currency", "rate", "date")
    list_filter = ("base_currency", "target_currency", "date")
    search_fields = ("base_currency__code", "target_currency__code")
