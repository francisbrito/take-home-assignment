from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "creates or updates local developer information from Github"
    requires_migrations_checks = True

    def handle(self, *args, **options) -> None:
        # TODO: implement this.
        raise NotImplementedError
