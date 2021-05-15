import os

from injector import Module, provider, singleton, threadlocal
from dataclasses import dataclass
from hvac import Client


@dataclass
class VaultConfiguration:
    url: str
    token: str


class VaultConfigurationModule(Module):
    @singleton
    @provider
    def provide_env_config(self) -> VaultConfiguration:
        return VaultConfiguration(
            url=os.getenv('VAULT_URL'),
            token=os.getenv('VAULT_TOKEN')
        )


class VaultModule(Module):
    @threadlocal
    @provider
    def provide_authed_hvac_client(self, config: VaultConfiguration) -> Client:
        client = Client(
            url=config.url,
            token=config.token,
        )
        client.kv.default_kv_version = 2
        assert client.is_authenticated()
        return client
