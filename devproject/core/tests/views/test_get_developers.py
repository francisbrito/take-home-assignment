import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from devproject.core.api.views import get_developers_view
from devproject.core.tests.factories import Developer

pytestmark = pytest.mark.django_db


def test_returns_a_list_of_developers_registered(request_factory):
    Developer.create(login="francisbrito", name="Francis Brito")
    Developer.create(login="kengru", name="Ken Grullon")

    path = reverse("api:get_developers")
    request = request_factory.get(path=path)
    response: Response = get_developers_view(request=request)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    assert len(response.data) == 2
    assert response.data[0]["login"] == "francisbrito"
    assert response.data[1]["login"] == "kengru"
