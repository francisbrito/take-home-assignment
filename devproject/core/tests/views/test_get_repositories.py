import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from devproject.core.api.views import get_repositories_view
from devproject.core.tests.factories import Repository

pytestmark = pytest.mark.django_db


def test_it_returns_a_list_of_repositories(request_factory):
    Repository.create(full_name="django/django")
    Repository.create(full_name="facebook/react")

    path = reverse("api:get_repositories")
    request = request_factory.get(path=path)
    response: Response = get_repositories_view(request=request)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    assert len(response.data) == 2
    assert response.data[0]["full_name"] == "django/django"
    assert response.data[1]["full_name"] == "facebook/react"
