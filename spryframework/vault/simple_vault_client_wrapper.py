from hvac import Client
from injector import inject


class SimpleVaultClientWrapper:
    @inject
    def __init__(self, vault_client: Client):
        self._vault_client = vault_client

    def get_kv_secrets(self, path: str, mount_point: str = 'kv'):
        return self._vault_client.secrets.kv.v2.read_secret_version(path, mount_point=mount_point)['data']['data']
