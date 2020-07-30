from django.conf import settings
from django.utils import timezone
from github import Github, UnknownObjectException, GithubException
from github.NamedUser import NamedUser

from devproject.core.models import Developer, Repository

_github = Github(login_or_token=settings.GITHUB_ACCESS_TOKEN)


def sync_developer(*, login: str) -> Developer:
    """
    Retrieves user information from Github and creates or updates developer information locally.
    :param login:  Github username of the developer
    :return:
    """

    try:
        response = _github.get_user(login=login)
        parsed_response = _parse_get_developer_response(response=response)
        developer = Developer.objects.filter(login=login).first()

        if developer is None:
            developer = Developer()

        for attr, value in parsed_response.items():
            setattr(developer, attr, value)

        developer.save()

        return developer
    except UnknownObjectException:
        raise Developer.DoesNotExist
    except GithubException:
        raise Developer.UnableToSync


def _parse_get_developer_response(response: NamedUser) -> dict:
    return {
        "avatar_url": response.avatar_url,
        "bio": response.bio,
        "company": response.company,
        "email": response.email,
        "hireable": response.hireable,
        "location": response.location,
        "login": response.login,
        "name": response.name,
        "url": response.url,
        "github_id": response.id,
        "github_node_id": response.node_id,
        "raw": response.raw_data,
        "created_at": timezone.make_aware(response.created_at)
        if timezone.is_naive(response.created_at)
        else response.created_at,
        "updated_at": timezone.make_aware(response.updated_at)
        if timezone.is_naive(response.updated_at)
        else response.updated_at,
    }


def sync_repository(*, name: str) -> Repository:
    """
    Retrieves repository information from Github and creates or updates repository information locally.
    :param name:
    :return:
    """
    # TODO: raise if repository is not found.
    # TODO: raise if an internal error occurs while syncing.
    raise NotImplementedError
