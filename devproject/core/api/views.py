from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, viewsets

from devproject.core import models
from devproject.core.api.exceptions import APIErrorsMixin
from devproject.core.selectors import (
    get_registered_developers,
    get_registered_repositories,
    get_repository_by_full_name,
)


class Developer(serializers.ModelSerializer):
    class Meta:
        model = models.Developer
        exclude = ("id", "created_at", "updated_at", "raw")


class Repository(serializers.ModelSerializer):
    class Meta:
        model = models.Repository
        exclude = ("id", "created_at", "updated_at", "raw")


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
class GetDevelopers(APIErrorsMixin, viewsets.ReadOnlyModelViewSet):
    queryset = get_registered_developers()
    serializer_class = Developer
    lookup_field = "login"


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_id="get_repositories",
        operation_summary="Get repositories",
        operation_description="Retrieves a list of repositories",
        tags=["repositories"],
        responses={"200": Repository(many=True)},
        security=[],
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_id="get_repository",
        operation_summary="Get repository",
        operation_description="Retrieves information about a repository given its full name",
        tags=["repositories"],
        responses={"200": Repository()},
        security=[],
    ),
)
class GetRepositories(APIErrorsMixin, viewsets.ReadOnlyModelViewSet):
    queryset = get_registered_repositories()
    serializer_class = Repository

    def get_object(self):
        full_name = f"{self.kwargs['owner']}/{self.kwargs['name']}"

        return get_repository_by_full_name(full_name=full_name)


get_developers_view = GetDevelopers.as_view({"get": "list"})
get_developer_view = GetDevelopers.as_view({"get": "retrieve"})

get_repositories_view = GetRepositories.as_view({"get": "list"})
get_repository_view = GetRepositories.as_view({"get": "retrieve"})
