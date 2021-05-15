import pickle

import pytest
from injector import Injector

from spryframework.vault.vault_module import VaultConfigurationModule, VaultModule

from hvac import Client


@pytest.fixture
def injector_object() -> Injector:
    injector = Injector([VaultConfigurationModule(), VaultModule()])
    return injector


@pytest.fixture
def vault_client(injector_object) -> Client:
    return injector_object.get(Client)


def test_injector_injects_authed_vault_client(vault_client):
    assert vault_client.is_authenticated()


def test_client_gets_secret_from_vault(vault_client):
    assert vault_client.secrets.kv.v2.read_secret_version('test', mount_point='kv')['data']['data']['TEST'] == 'TEST'


def test_injector_can_be_pickled(injector_object):
    pickled_injector = pickle.dumps(injector_object)
    injector2 = pickle.loads(pickled_injector)  # type: Injector
    client = injector2.get(Client)
    test_injector_injects_authed_vault_client(client)
