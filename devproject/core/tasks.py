from celery import shared_task

from devproject.core import services


@shared_task
def sync_repository(full_name: str) -> None:
    services.sync_repository(full_name=full_name)


@shared_task
def sync_developer(login: str) -> None:
    services.sync_developer(login=login)
