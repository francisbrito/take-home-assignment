from django.core.management.base import BaseCommand
from django_celery_beat.models import CrontabSchedule, IntervalSchedule, PeriodicTask

from devproject.core.tasks import (
    sync_registered_developers,
    sync_registered_repositories,
)


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        self.stdout.write(self.style.WARNING("deleting existing periodic tasks"))

        _delete_existing_periodic_tasks()

        periodic_tasks = [
            {
                "task": sync_registered_developers,
                "name": "Sync registered developers daily",
                "cron": {
                    "minute": "0",
                    "hour": "0",
                    "day_of_week": "*",
                    "day_of_month": "*",
                    "month_of_year": "*",
                },
                "enabled": True,
            },
            {
                "task": sync_registered_repositories,
                "name": "Sync registered repositories daily",
                "cron": {
                    "minute": "0",
                    "hour": "0",
                    "day_of_week": "*",
                    "day_of_month": "*",
                    "month_of_year": "*",
                },
                "enabled": True,
            },
        ]

        for task in periodic_tasks:
            cron = CrontabSchedule.objects.create(**task["cron"])

            PeriodicTask.objects.create(
                name=task["name"],
                task=task["task"],
                crontab=cron,
                enabled=task["enabled"],
            )

            self.stdout.write(
                f"'{task['name']}' ... " + self.style.SUCCESS("REGISTERED")
            )


def _delete_existing_periodic_tasks():
    IntervalSchedule.objects.all().delete()
    CrontabSchedule.objects.all().delete()
    PeriodicTask.objects.all().delete()
