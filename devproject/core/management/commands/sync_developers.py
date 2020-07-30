import sys
import traceback

from django.core.management.base import BaseCommand, CommandParser

from devproject.core.selectors import get_registered_developers
from devproject.core.services import sync_developer

ERROR_CODE_MISSING_INPUT = 1


class Command(BaseCommand):
    help = "creates or updates local developer information from Github"
    requires_migrations_checks = True

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("logins", nargs="*", type=str)
        parser.add_argument(
            "-r",
            "--registered",
            action="store_true",
            help="use registered developers as input",
        )

    def handle(self, *args, **options) -> None:
        if options["registered"]:
            options["logins"] = get_registered_developers().values_list(
                "login", flat=True
            )

        if len(options["logins"]) == 0:
            self.stdout.write(
                self.style.ERROR(
                    "either provide an space-separated list of logins or pass --registered flag"
                )
            )

            sys.exit(ERROR_CODE_MISSING_INPUT)

        for login in options["logins"]:
            self.stdout.write(f"syncing developer '{login}' ... ", ending="")

            try:
                sync_developer(login=login)

                self.stdout.write(self.style.SUCCESS("SUCCESS"))
            except Exception as e:  # noqa
                self.stdout.write(self.style.ERROR("FAILED"))
                self.stderr.write(traceback.format_exc())
