from django.urls import path
from .views import convert_currency, conversion_history

urlpatterns = [
    path("", convert_currency, name="convert"),
    path("history/", conversion_history, name="conversion_history"),
]