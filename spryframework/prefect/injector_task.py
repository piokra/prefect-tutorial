from injector import Injector
from prefect import task

from spryframework.influxdb2.influxdb2_module import InfluxDB2ConfigModule, InfluxDB2Module
from spryframework.vault.vault_module import VaultModule, VaultConfigurationModule


@task
def create_secret_injector_task():
    return Injector([VaultConfigurationModule(), VaultModule(), InfluxDB2ConfigModule(), InfluxDB2Module()])
