import factory
import pytest
from github import UnknownObjectException, GithubException, NamedUser

from devproject.core import models
from devproject.core.services import sync_developer
from devproject.core.tests.factories import Developer

pytestmark = pytest.mark.django_db


def test_it_raises_if_user_with_given_login_does_not_exist(mocker):
    gh_mock = mocker.patch("devproject.core.services._github")
    gh_mock.get_user = mocker.MagicMock(
        side_effect=UnknownObjectException(status=404, data={"message": "Not Found"})
    )

    with pytest.raises(models.Developer.DoesNotExist):
        sync_developer(login="francisbrito")


def test_it_raises_if_an_internal_github_exception_is_raised(mocker):
    gh_mock = mocker.patch("devproject.core.services._github")
    gh_mock.get_user = mocker.MagicMock(
        side_effect=GithubException(status=500, data={"message": "Internal Error"})
    )

    with pytest.raises(models.Developer.UnableToSync):
        sync_developer(login="francisbrito")


def test_it_registers_developer_if_its_not_registered(mocker):
    gh_user_response_mock: NamedUser = _create_mock_user_response(
        mocker, login="francisbrito"
    )
    gh_mock = mocker.patch("devproject.core.services._github")
    gh_mock.get_user = mocker.MagicMock(return_value=gh_user_response_mock)

    sync_developer(login="francisbrito")

    assert models.Developer.objects.count() == 1
    assert models.Developer.objects.first().login == "francisbrito"


def test_it_updates_developer_if_its_already_registered(mocker):
    original: models.Developer = Developer.create(
        login="francisbrito", name="Francis Brito"
    )
    gh_user_response_mock = _create_mock_user_response(mocker, login="francisbrito")
    gh_mock = mocker.patch("devproject.core.services._github")
    gh_mock.get_user = mocker.MagicMock(return_value=gh_user_response_mock)
    updated = sync_developer(login="francisbrito")

    assert original.name != updated.name

    original.refresh_from_db()

    assert original.name == updated.name


def _create_mock_user_response(mocker, **kwargs):
    gh_user_response_mock: NamedUser = factory.build(
        mocker.MagicMock, FACTORY_CLASS=Developer, **kwargs
    )
    gh_user_response_mock.raw_data = gh_user_response_mock.raw
    gh_user_response_mock.node_id = gh_user_response_mock.github_node_id
    gh_user_response_mock.id = gh_user_response_mock.github_id
    gh_user_response_mock.login = gh_user_response_mock.login

    for attr, value in kwargs.items():
        setattr(gh_user_response_mock, attr, value)

    return gh_user_response_mock
