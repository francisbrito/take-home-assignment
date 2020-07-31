from django.db.models import QuerySet

from devproject.core.models import Developer, Repository


def get_registered_developers() -> "QuerySet[Developer]":
    """
    Retrieves a queryset with all the developers registered locally sorted by login.
    :return: a Developer queryset.
    """
    return Developer.objects.all().order_by("login")


def get_registered_repositories() -> "QuerySet[Repository]":
    """
    Retrieves a queryset with all the repositories registered locally sorted by full name.
    :return: a Repository queryset.
    """
    return Repository.objects.all().order_by("full_name")


def get_repository_by_full_name(*, full_name: str) -> Repository:
    """
    Retrieves a repository by its full_name.
    :param full_name:
    :return: a Repository.
    """
    return Repository.objects.get(full_name=full_name)  # noqa
