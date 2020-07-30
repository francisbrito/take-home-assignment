import sys
import traceback

from django.core.management.base import BaseCommand, CommandParser

from devproject.core.selectors import get_registered_repositories
from devproject.core.services import sync_repository

ERROR_CODE_INVALID_INPUT = 1


class Command(BaseCommand):
    help = "creates or updates local repository information from Github"
    requires_migrations_checks = True

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("repo_full_names", nargs="*", type=str)
        parser.add_argument(
            "-r",
            "--registered",
            action="store_true",
            help="use registered repositories as input",
        )

    def handle(self, *args, **options) -> None:
        if options["registered"]:
            options["repo_full_names"] = get_registered_repositories().values_list(
                "full_name", flat=True
            )

        if len(options["repo_full_names"]) == 0:
            self.stdout.write(
                self.style.ERROR(
                    "either provide a space-separated list of repo full names or provide --registered flag"
                )
            )

            sys.exit(ERROR_CODE_INVALID_INPUT)

        for full_name in options["repo_full_names"]:
            self.stdout.write(f"syncing repository '{full_name}' ... ", ending="")

            try:
                sync_repository(full_name=full_name)

                self.stdout.write(self.style.SUCCESS("SUCCESS"))
            except Exception as e:  # noqa
                self.stdout.write(self.style.ERROR("FAILED"))
                self.stderr.write(traceback.format_exc())
