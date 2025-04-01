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
