import pytest

from devproject.core import models
from devproject.core.selectors import get_registered_developers
from devproject.core.tests.factories import Developer

pytestmark = pytest.mark.django_db


def test_it_returns_a_queryset_of_registered_developers():
    assert get_registered_developers().count() == 0

    new_dev: models.Developer = Developer.create()

    assert get_registered_developers().count() == 1
    assert get_registered_developers().first().login == new_dev.login
