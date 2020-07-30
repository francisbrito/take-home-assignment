import traceback

from django.core.management.base import BaseCommand, CommandParser

from devproject.core.services import sync_repository


class Command(BaseCommand):
    help = "creates or updates local repository information from Github"
    requires_migrations_checks = True

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("repo_full_names", nargs="+", type=str)

    def handle(self, *args, **options) -> None:
        for full_name in options["repo_full_names"]:
            self.stdout.write(f"syncing repository '{full_name}' ... ", ending="")

            try:
                sync_repository(full_name=full_name)

                self.stdout.write(self.style.SUCCESS("SUCCESS"))
            except Exception as e:  # noqa
                self.stdout.write(self.style.ERROR("FAILED"))
                self.stderr.write(traceback.format_exc())
