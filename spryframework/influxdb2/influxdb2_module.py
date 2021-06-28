from dataclasses import dataclass

import influxdb_client
from injector import provider, threadlocal, singleton, Module

from spryframework.vault.simple_vault_client_wrapper import SimpleVaultClientWrapper


@dataclass
class InfluxDBConfigV2:
    url: str
    token: str
    org: str


class InfluxDB2ConfigModule(Module):
    @singleton
    @provider
    def provide_vault_config_v2(self, vault: SimpleVaultClientWrapper) -> InfluxDBConfigV2:
        d = vault.get_kv_secrets('common', 'kv')
        return InfluxDBConfigV2(
            url=d['INFLUX_V2_URL'],
            org=d['INFLUX_V2_ORG'],
            token=d['INFLUX_V2_TOKEN']
        )


class InfluxDB2Module(Module):
    @threadlocal
    @provider
    def provide_influxdb_v2_client(self, config: InfluxDBConfigV2) -> influxdb_client.InfluxDBClient:
        return influxdb_client.InfluxDBClient(
            url=config.url,
            token=config.token,
            org=config.org
        )
