from django.db.models import QuerySet

from devproject.core.models import Developer


def get_registered_developers() -> "QuerySet[Developer]":
    """
    Retrieves a queryset with all the developers registered locally sorted by login.
    :return: a Developer queryset.
    """
    return Developer.objects.all().order_by("login")
