from influxdb import InfluxDBClient, DataFrameClient
import influxdb_client

from injector import Module, provider, singleton, threadlocal
from dataclasses import dataclass

from spryframework.influxdb2.influxdb2_module import InfluxDBConfigV2
from spryframework.vault.simple_vault_client_wrapper import SimpleVaultClientWrapper


@dataclass
class InfluxDBConfig:
    host: str
    username: str
    password: str
    database: str


class InfluxDBConfigModule(Module):
    @singleton
    @provider
    def provide_vault_config(self, vault: SimpleVaultClientWrapper) -> InfluxDBConfig:
        d = vault.get_kv_secrets('common', 'kv')
        return InfluxDBConfig(
            host=d['INFLUX_HOST'],
            username=d['INFLUX_USER'],
            password=d['INFLUX_PASSWORD'],
            database=d['INFLUX_DATABASE']
        )


class InfluxDBModule(Module):
    @threadlocal
    @provider
    def provide_influxdb_client(self, config: InfluxDBConfig) -> InfluxDBClient:
        return InfluxDBClient(
            host=config.host,
            username=config.username,
            password=config.password,
            database=config.database
        )

    @threadlocal
    @provider
    def provide_influxdb_dataframe_client(self, config: InfluxDBConfig) -> DataFrameClient:
        return DataFrameClient(
            host=config.host,
            username=config.username,
            password=config.password,
            database=config.database
        )
