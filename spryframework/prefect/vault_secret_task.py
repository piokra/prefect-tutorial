from injector import Injector
from prefect import task

from spryframework.vault.simple_vault_client_wrapper import SimpleVaultClientWrapper


@task
def fetch_secret_task(path: str, mount_point: str, injector: Injector):
    secret_fetcher = injector.get(SimpleVaultClientWrapper)
    return secret_fetcher.get_kv_secrets(path, mount_point)
