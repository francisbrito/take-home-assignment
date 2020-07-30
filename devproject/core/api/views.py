from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, viewsets

from devproject.core import models
from devproject.core.selectors import get_registered_developers


class Developer(serializers.ModelSerializer):
    class Meta:
        model = models.Developer
        exclude = ("id", "created_at", "updated_at")


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_id="get_developers",
        operation_summary="Get developers",
        operation_description="Retrieves a list of developers",
        tags=["developers"],
        responses={"200": Developer(many=True)},
        security=[],
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_id="get_developer",
        operation_summary="Get developer",
        operation_description="Retrieves information about a developer by its login",
        tags=["developers"],
        responses={"200": Developer()},
        security=[],
    ),
)
class GetDevelopers(viewsets.ReadOnlyModelViewSet):
    queryset = get_registered_developers()
    serializer_class = Developer
    lookup_field = "login"


get_developers_view = GetDevelopers.as_view({"get": "list"})
get_developer_view = GetDevelopers.as_view({"get": "retrieve"})
