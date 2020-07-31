from rest_framework import exceptions as rest_exceptions
from rest_framework.exceptions import ValidationError

from devproject.core import models


class APIErrorsMixin:
    """
    Mixin that transforms Django and Python exceptions into rest_framework ones.
    without the mixin, they return 500 status code which is not desired.

    Take from HackSoftware's Django StyleGuide:

    https://github.com/HackSoftware/Styleguide-Example/blob/master/styleguide_example/api/mixins.py
    """

    expected_exceptions = {
        ValueError: rest_exceptions.ValidationError,
        ValidationError: rest_exceptions.ValidationError,
        PermissionError: rest_exceptions.PermissionDenied,
        models.Developer.DoesNotExist: rest_exceptions.NotFound,
        models.Repository.DoesNotExist: rest_exceptions.NotFound,
    }

    def handle_exception(self, exc):
        if isinstance(exc, tuple(self.expected_exceptions.keys())):
            drf_exception_class = self.expected_exceptions[exc.__class__]
            drf_exception = drf_exception_class(exc)

            return super().handle_exception(drf_exception)

        return super().handle_exception(exc)
