from django.contrib.auth.models import User
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    class Meta:
        abstract = True


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name="Код валюты")
    name = models.CharField(max_length=100, verbose_name="Название")
    symbol = models.CharField(max_length=10, blank=True, null=True, verbose_name="Символ")

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class ExchangeRate(models.Model):
    base_currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="base_rates", verbose_name="Базовая валюта"
    )
    target_currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="target_rates", verbose_name="Целевая валюта"
    )
    rate = models.DecimalField(max_digits=20, decimal_places=6, verbose_name="Курс")
    date = models.DateField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        unique_together = ("base_currency", "target_currency", "date")
        verbose_name = "Курс обмена"
        verbose_name_plural = "Курсы обмена"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.base_currency.code} → {self.target_currency.code}: {self.rate}"


class ConversionHistory(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Сумма")
    from_currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="history_from", verbose_name="Из валюты"
    )
    to_currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="history_to", verbose_name="В валюту"
    )
    converted_amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Сконвертировано")

    class Meta:
        verbose_name = "История конвертации"
        verbose_name_plural = "История конвертаций"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}: {self.amount} {self.from_currency} → {self.to_currency} = {self.converted_amount}"


class FavoriteConversionDirection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    from_currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="favorite_from", verbose_name="Из валюты"
    )
    to_currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="favorite_to", verbose_name="В валюту"
    )

    class Meta:
        unique_together = ("user", "from_currency", "to_currency")
        verbose_name = "Избранное направление"
        verbose_name_plural = "Избранные направления"
        ordering = ["user", "from_currency__code", "to_currency__code"]

    def __str__(self):
        return f"{self.user.username}: {self.from_currency.code} → {self.to_currency.code}"
