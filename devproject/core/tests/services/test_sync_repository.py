import factory
import pytest
from github import (
    UnknownObjectException,
    GithubException,
    Repository as GithubRepository,
)

from devproject.core import models
from devproject.core.services import sync_repository
from devproject.core.tests.factories import Repository

pytestmark = pytest.mark.django_db


def test_it_raises_if_repository_with_given_name_does_not_exist(mocker):
    gh_mock = mocker.patch("devproject.core.services._github")
    gh_mock.get_repo = mocker.MagicMock(
        side_effect=UnknownObjectException(status=404, data={"message": "Not Found"})
    )

    with pytest.raises(models.Repository.DoesNotExist):
        sync_repository(full_name="django/django")


def test_it_raises_if_an_internal_exception_is_raised(mocker):
    gh_mock = mocker.patch("devproject.core.services._github")
    gh_mock.get_repo = mocker.MagicMock(
        side_effect=GithubException(status=500, data={"message": "Internal Error"})
    )

    with pytest.raises(models.Repository.UnableToSync):
        sync_repository(full_name="django/django")


def test_it_register_a_repository_if_not_already_registered(mocker):
    gh_repo_response_mock = _create_mock_repo_response(
        mocker, name="django", full_name="django/django"
    )
    gh_mock = mocker.patch("devproject.core.services._github")
    gh_mock.get_repo = mocker.MagicMock(return_value=gh_repo_response_mock)

    sync_repository(full_name="django/django")

    assert models.Repository.objects.count() == 1
    assert models.Repository.objects.first().full_name == "django/django"


def test_it_updates_repository_if_its_already_registered(mocker):
    original: models.Repository = Repository.create(full_name="django/django")
    gh_repo_response_mock = _create_mock_repo_response(
        mocker, full_name="django/django", description="Django Project",
    )
    gh_mock = mocker.patch("devproject.core.services._github")
    gh_mock.get_repo = mocker.MagicMock(return_value=gh_repo_response_mock)
    updated = sync_repository(full_name="django/django")

    assert updated.description
    assert original.description != updated.description

    original.refresh_from_db()

    assert original.description == updated.description


def _create_mock_repo_response(mocker, **kwargs) -> GithubRepository:
    mock = factory.build(mocker.MagicMock, FACTORY_CLASS=Repository)
    mock.raw_data = mock.raw
    mock.node_id = mock.github_node_id
    mock.id = mock.github_id
    mock.name = mock.name
    mock.full_name = mock.full_name
    mock.name = mock.full_name.split("/")[1]

    for attr, value in kwargs.items():
        setattr(mock, attr, value)

    return mock
