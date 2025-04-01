from django.urls import path

from . import views

urlpatterns = [
    path("", views.convert_currency, name="convert"),
    path("history/", views.conversion_history, name="conversion_history"),
    path(
        "favorite/add/<str:from_code>/<str:to_code>/",
        views.add_to_favorites,
        name="add_to_favorites",
    ),
    path(
        "favorite/remove/<str:from_code>/<str:to_code>/",
        views.remove_from_favorites,
        name="remove_from_favorites",
    ),
]
