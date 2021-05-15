from injector import Injector
from prefect import task

from spryframework.vault.vault_module import VaultModule, VaultConfigurationModule


@task
def create_secret_injector_task():
    return Injector([VaultConfigurationModule(), VaultModule()])
