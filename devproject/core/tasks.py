from celery import shared_task

from devproject.core import selectors, services


@shared_task
def sync_repository(full_name: str) -> None:
    services.sync_repository(full_name=full_name)


@shared_task
def sync_developer(login: str) -> None:
    services.sync_developer(login=login)


@shared_task
def sync_registered_developers() -> None:
    for dev in selectors.get_registered_developers():
        sync_developer.delay(login=dev.login)


@shared_task
def sync_registered_repositories() -> None:
    for repo in selectors.get_registered_repositories():
        sync_repository.delay(full_name=repo.full_name)
