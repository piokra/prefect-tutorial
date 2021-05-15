from datetime import timedelta
from typing import Dict

import prefect
from prefect import task, Flow, Parameter, unmapped
from prefect.schedules import IntervalSchedule
from prefect.storage import GitHub
from prefect.tasks.secrets import EnvVarSecret

from alpha_vantage.timeseries import TimeSeries

from spryframework.prefect.injector_task import create_secret_injector_task
from spryframework.prefect.vault_secret_task import fetch_secret_task


@task
def scrap_stock(stock: str, secrets: Dict[str, str]):
    logger = prefect.context.get("logger")
    logger.info(f"Scrapping {stock}!")
    ts = TimeSeries(key=secrets['ALPHA_VANTAGE_TOKEN'])
    # Get json object with the intraday data and another with  the call's metadata
    data, meta_data = ts.get_intraday(stock)
    logger.info(data)
    logger.info(meta_data)
    return data, meta_data


schedule = IntervalSchedule(interval=timedelta(hours=24))

with Flow("scrap-stock", schedule) as flow:
    injector = create_secret_injector_task()
    secrets = fetch_secret_task('common', 'kv', injector)
    stocks = Parameter("stocks", default=["GOOGL", "MSFT"])
    scrap_stock.map(stocks, secrets=unmapped(secrets))

flow.storage = GitHub(
    repo="piokra/prefect-tutorial",
    path="scrap-stock.py"
)

flow.run()
