import pytest
from hvac import Client
from injector import Injector

from spryframework.influxdb.influxdb_module import InfluxDBModule, InfluxDBConfigModule
from spryframework.influxdb2.influxdb2_module import InfluxDB2ConfigModule, InfluxDB2Module
from spryframework.vault.vault_module import VaultConfigurationModule, VaultModule


@pytest.fixture
def injector_object() -> Injector:
    injector = Injector([
        VaultConfigurationModule(),
        VaultModule(),
        InfluxDBModule(),
        InfluxDBConfigModule(),
        InfluxDB2ConfigModule(),
        InfluxDB2Module()])
    return injector


@pytest.fixture
def vault_client(injector_object) -> Client:
    return injector_object.get(Client)
