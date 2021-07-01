from datetime import timedelta
from typing import Dict

import prefect
from influxdb_client import Point, InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from injector import Injector
from prefect import task, Flow, Parameter, unmapped
from prefect.schedules import IntervalSchedule
from prefect.storage import GitHub
from prefect.tasks.secrets import EnvVarSecret

from alpha_vantage.timeseries import TimeSeries

from models.av_models import InterdayResponseModel, interday_response_model_to_points
from spryframework.prefect.injector_task import create_secret_injector_task
from spryframework.prefect.vault_secret_task import fetch_secret_task, renew_token_task


@task
def scrap_stock(stock: str, secrets: Dict[str, str]) -> InterdayResponseModel:
    logger = prefect.context.get("logger")
    logger.info(f"Scrapping {stock}!")
    ts = TimeSeries(key=secrets['ALPHA_VANTAGE_TOKEN'])
    # Get json object with the intraday data and another with  the call's metadata
    data, meta_data = ts.get_intraday(stock)
    logger.info(data)
    logger.info(meta_data)
    return InterdayResponseModel.parse_obj({
        "Meta Data": meta_data,
        "Time Series (15min)": data
    })


@task
def persist_data_in_influx(injector: Injector, av_response: InterdayResponseModel, secrets: Dict[str, str]):
    influx_v2_client = injector.get(InfluxDBClient)
    influx_v2_client.write_api(SYNCHRONOUS).write(secrets['INFLUX_V2_BUCKET'],
                                                  record=interday_response_model_to_points(av_response))


schedule = IntervalSchedule(interval=timedelta(hours=24))

with Flow("scrap-stock", schedule) as flow:
    injector = create_secret_injector_task()
    token_renewal_result = renew_token_task(injector)
    secrets = fetch_secret_task('common', 'kv', injector)
    stocks = Parameter("stocks", default=["GOOGL", "MSFT"])
    av_response = scrap_stock.map(stocks, secrets=unmapped(secrets))
    persist_data_in_influx(injector, av_response, secrets)

flow.storage = GitHub(
    repo="piokra/prefect-tutorial",
    path="scrap_stock.py"
)

flow.run()
