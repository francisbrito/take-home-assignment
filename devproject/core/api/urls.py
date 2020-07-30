from django.urls import path

from devproject.core.api.views import get_developer_view, get_developers_view

urlpatterns = [
    path("", get_developers_view, name="get_developers"),
    path("<str:login>/", get_developer_view, name="get_developer"),
]
