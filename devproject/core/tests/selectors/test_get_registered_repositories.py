import pytest

from devproject.core.selectors import get_registered_repositories
from devproject.core.tests.factories import Repository

pytestmark = pytest.mark.django_db


def test_it_returns_a_queryset_of_registered_repositories():
    assert get_registered_repositories().count() == 0

    new_repo = Repository.create()

    assert get_registered_repositories().count() == 1
    assert get_registered_repositories().first().full_name == new_repo.full_name
