from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Tesorio Developer Registry",
        default_version="v1",
        description="A demo take-home assignment for backend position candidates",
        contact=openapi.Contact(email="francis@brito.do"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

app_name = "api"
urlpatterns = [
    path("", include("devproject.core.api.urls")),
    path(
        "documentation/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    re_path(
        r"^openapi(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
]
