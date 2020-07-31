import pytest
from rest_framework.test import APIRequestFactory

from devproject.users.models import User
from devproject.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def request_factory() -> APIRequestFactory:
    return APIRequestFactory(enforce_csrf_checks=False)
