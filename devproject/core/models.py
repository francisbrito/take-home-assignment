from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _


class ValidateOnSaveMixin:
    """
    Mixin to validate model whenever its save method is called.
    """

    def save(self, *args, **kwargs):
        self.full_clean()

        return super(ValidateOnSaveMixin, self).save(*args, **kwargs)


class GithubEntity(models.Model):
    """
    Represents any github entity.
    """

    github_id = models.BigIntegerField(verbose_name=_("Github ID"), unique=True)
    github_node_id = models.CharField(
        verbose_name=_("Github Node ID"), max_length=50, unique=True
    )
    created_at = models.DateTimeField(verbose_name=_("Created at"), editable=False)
    updated_at = models.DateTimeField(verbose_name=_("Updated at"), editable=False)
    url = models.URLField(verbose_name=_("URL"), max_length=1000, editable=False)
    raw = JSONField(verbose_name=_("Raw"), editable=False)

    class Meta:
        abstract = True


class Developer(ValidateOnSaveMixin, GithubEntity):
    """
    Represents any user of the Github platform.
    """

    login = models.CharField(verbose_name=_("Login"), max_length=100, unique=True)
    avatar_url = models.URLField(verbose_name=_("Avatar URL"), blank=True, null=True)
    name = models.CharField(
        verbose_name=_("Name"), max_length=100, blank=True, null=True
    )
    company = models.CharField(
        verbose_name=_("Company"), max_length=100, blank=True, null=True
    )
    location = models.CharField(
        verbose_name=_("Location"), max_length=250, blank=True, null=True
    )
    email = models.EmailField(
        verbose_name=_("E-mail"), max_length=250, blank=True, null=True, unique=True
    )
    hireable = models.BooleanField(
        verbose_name=_("Can be hired?"), blank=True, null=True
    )
    bio = models.TextField(
        verbose_name=_("Biography"), max_length=1000, blank=True, null=True
    )

    class Meta:
        verbose_name = _("developer")
        verbose_name_plural = _("developers")

    class UnableToSync(Exception):
        pass


class Repository(ValidateOnSaveMixin, GithubEntity):
    """
    Represents a code base in the Github platform.
    """

    name = models.CharField(verbose_name=_("Name"), max_length=250, unique=True)
    full_name = models.CharField(
        verbose_name=_("Full name"), max_length=250, unique=True
    )
    private = models.BooleanField(verbose_name=_("Private?"), blank=True, default=False)
    description = models.TextField(
        verbose_name=_("Description"), max_length=1000, blank=True, null=True
    )
