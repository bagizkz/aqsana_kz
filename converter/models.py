from django.contrib.auth.models import User
from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class ExchangeRate(models.Model):
    base_currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="base_rates"
    )
    target_currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="target_rates"
    )
    rate = models.DecimalField(max_digits=20, decimal_places=6)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("base_currency", "target_currency", "date")

    def __str__(self):
        return f"{self.base_currency.code} → {self.target_currency.code}: {self.rate}"


class ConversionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    from_currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="history_from"
    )
    to_currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="history_to"
    )
    converted_amount = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.amount} {self.from_currency} → {self.to_currency} = {self.converted_amount}"


class FavoriteConversionDirection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="favorite_from"
    )
    to_currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="favorite_to"
    )

    class Meta:
        unique_together = ("user", "from_currency", "to_currency")

    def __str__(self):
        return (
            f"{self.user.username}: {self.from_currency.code} → {self.to_currency.code}"
        )
