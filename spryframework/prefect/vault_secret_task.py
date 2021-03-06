from hvac import Client
from injector import Injector
from prefect import task

from spryframework.vault.simple_vault_client_wrapper import SimpleVaultClientWrapper


@task
def fetch_secret_task(path: str, mount_point: str, injector: Injector):
    secret_fetcher = injector.get(SimpleVaultClientWrapper)  # Not sure if Injector is pickleable
    return secret_fetcher.get_kv_secrets(path, mount_point)


@task
def renew_token_task(injector: Injector):
    client = injector.get(Client)
    return client.renew_self_token()
