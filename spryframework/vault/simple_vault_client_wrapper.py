from typing import Dict, Union, Tuple, Callable

from hvac import Client
from injector import inject, Module, singleton, provider


class SimpleVaultClientWrapper:
    @inject
    def __init__(self, vault_client: Client):
        self._vault_client = vault_client

    def get_kv_secrets(self, path: str, mount_point: str = 'kv') -> Dict[str, str]:
        return self._vault_client.secrets.kv.v2.read_secret_version(path, mount_point=mount_point)['data']['data']


class MockedSimpleVaultClientWrapper(SimpleVaultClientWrapper):
    def __init__(self, secrets: Dict[str,
                                     Dict[str, str]
    ]):
        self._secrets = secrets

    def get_kv_secrets(self, path: str, mount_point: str = 'kv') -> Dict[str, str]:
        return self._secrets[path]


class MockedSimpleVaultClientService(Module):
    def __init__(self,
                 secrets: Dict[str,
                               Dict[str, str]
                 ]):
        self._secrets = secrets

    @singleton
    @provider
    def provide_mocked_vault_wrapper(self) -> SimpleVaultClientWrapper:
        return MockedSimpleVaultClientWrapper(self._secrets)
