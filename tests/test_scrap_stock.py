from influxdb_client.client.write_api import SYNCHRONOUS

from models.av_models import interday_response_model_to_points
from resources.interday_15m_example import INTERDAY_15M_IBM_MODEL
from spryframework.tests.influxdb2.test_influxdb2_module import influx_v2_client, local_injector_object, \
    injector_object, clean_measurements
from tests.resources.config import TEST_CONFIG

FLUX_TEST_QUERY = f"""\
from(bucket: "{TEST_CONFIG['common']['INFLUX_V2_BUCKET']}")
|> range(start: 2021-06-23T13:00:00Z, stop: 2021-06-25T20:30:00Z)
|> filter(fn: (r) => r._measurement == "interday" and r._field == "volume")
"""


def test_persist_av_response_model_in_testing_influxdb(influx_v2_client, clean_measurements):
    influx_v2_client.write_api(SYNCHRONOUS).write('metrics',
                                                  record=interday_response_model_to_points(INTERDAY_15M_IBM_MODEL))
    influx_result = influx_v2_client.query_api().query(FLUX_TEST_QUERY)
    influx_set = {record.get_value() for table in influx_result for record in table.records}

    mock_set = {point.volume for point in INTERDAY_15M_IBM_MODEL.points.values()}
    assert influx_set == mock_set
