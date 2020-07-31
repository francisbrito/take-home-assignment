import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from devproject.core import models
from devproject.core.api.views import get_developer_view
from devproject.core.tests.factories import Developer

pytestmark = pytest.mark.django_db


def test_it_returns_information_about_a_single_developer(request_factory):
    developer: models.Developer = Developer.create(
        login="francisbrito", name="Francis Brito"
    )
    path = reverse("api:get_developer", kwargs={"login": developer.login})
    request = request_factory.get(path=path)
    response: Response = get_developer_view(request=request, login=developer.login)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, dict)
    assert response.data["login"] == developer.login
    assert response.data["name"] == developer.name


def test_it_returns_404_if_developer_not_found(request_factory):
    path = reverse("api:get_developer", kwargs={"login": "not_found"})
    request = request_factory.get(path=path)
    response: Response = get_developer_view(request=request, login="not_found")

    assert response.status_code == status.HTTP_404_NOT_FOUND
