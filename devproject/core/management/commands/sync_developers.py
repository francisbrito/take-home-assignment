import traceback

from django.core.management.base import BaseCommand, CommandParser

from devproject.core.services import sync_developer


class Command(BaseCommand):
    help = "creates or updates local developer information from Github"
    requires_migrations_checks = True

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("logins", nargs="+", type=str)

    def handle(self, *args, **options) -> None:
        for login in options["logins"]:
            self.stdout.write(f"syncing developer '{login}' ... ", ending="")

            try:
                sync_developer(login=login)

                self.stdout.write(self.style.SUCCESS("SUCCESS"))
            except Exception as e:  # noqa
                self.stdout.write(self.style.ERROR("FAILED"))
                self.stderr.write(traceback.format_exc())
