import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from devproject.core import models
from devproject.core.api.views import get_repository_view
from devproject.core.tests.factories import Repository

pytestmark = pytest.mark.django_db


def test_it_returns_information_about_a_single_repository(request_factory):
    repository: models.Repository = Repository.create(full_name="django/django")
    path = reverse("api:get_repository", kwargs={"owner": "django", "name": "django"})
    request = request_factory.get(path=path)
    response: Response = get_repository_view(
        request=request, owner="django", name="django"
    )

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, dict)
    assert response.data["full_name"] == repository.full_name
    assert response.data["name"] == repository.name


def test_it_returns_404_if_repository_not_found(request_factory):
    path = reverse("api:get_repository", kwargs={"owner": "not", "name": "found"})
    request = request_factory.get(path=path)
    response: Response = get_repository_view(request=request, owner="not", name="found")

    assert response.status_code == status.HTTP_404_NOT_FOUND
