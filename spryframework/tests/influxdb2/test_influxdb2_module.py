import pytest
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from injector import Injector, singleton

from spryframework.influxdb.influxdb_module import InfluxDBConfig
from spryframework.influxdb2.influxdb2_module import InfluxDBConfigV2
from spryframework.tests.vault.common_fixtures import injector_object
from spryframework.vault.simple_vault_client_wrapper import MockedSimpleVaultClientService
from tests.resources.config import TEST_CONFIG


@pytest.fixture
def local_injector_object(injector_object) -> Injector:
    injector_object.binder.install(MockedSimpleVaultClientService(TEST_CONFIG))
    return injector_object


@pytest.fixture
def influx_v2_client(local_injector_object) -> InfluxDBClient:
    return local_injector_object.get(InfluxDBClient)


@pytest.fixture
def example_point():
    return Point("test_measurement").tag("tag", "test").field("hello", 0).field("world", 1).time(1568808000000000000)


@pytest.fixture
def clean_measurements(influx_v2_client):
    start = "1970-01-01T00:00:00Z"
    stop = "2137-02-01T00:00:00Z"
    influx_v2_client.delete_api().delete(start, stop, predicate='_measurement="*"', org='testing',
                                         bucket='metrics')
    influx_v2_client.health()


def test_injector_provides_healthy_influxdb_client(influx_v2_client: InfluxDBClient):
    assert influx_v2_client.health().status == 'pass'


def test_influx_v2_able_to_write_point(influx_v2_client, example_point, clean_measurements):
    influx_v2_client.write_api(write_options=SYNCHRONOUS).write(bucket='metrics', record=example_point)
