from django.urls import path

from devproject.core.api.views import (
    get_developer_view,
    get_developers_view,
    get_repositories_view,
    get_repository_view,
)

urlpatterns = [
    path("developers/", get_developers_view, name="get_developers"),
    path("developers/<str:login>/", get_developer_view, name="get_developer"),
    path("repositories/", get_repositories_view, name="get_repositories"),
    path(
        "repositories/<str:owner>/<str:name>/",
        get_repository_view,
        name="get_repository",
    ),
]
