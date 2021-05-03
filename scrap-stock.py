from datetime import timedelta

import prefect
from prefect import task, Flow, Parameter
from prefect.schedules import IntervalSchedule
from prefect.storage import GitHub
from prefect.tasks.secrets import EnvVarSecret

from alpha_vantage.timeseries import TimeSeries
from prefect.utilities.tasks import unmapped


@task
def scrap_stock(stock: str, key: str):


    logger = prefect.context.get("logger")
    logger.info(f"Scrapping {stock}!")
    ts = TimeSeries(key=key)
    # Get json object with the intraday data and another with  the call's metadata
    data, meta_data = ts.get_intraday('GOOGL')
    logger.info(data)
    logger.info(meta_data)


schedule = IntervalSchedule(interval=timedelta(hours=24))

with Flow("scrap-stock", schedule) as flow:
    key = EnvVarSecret("AV_TOKEN")
    stocks = Parameter("stocks", default=["GOOGL", "MSFT"])
    scrap_stock.map(stocks, key=unmapped(key))

flow.storage = GitHub(
    repo="piokra/prefect-tutorial",
    path="scrap-stock.py"
)

flow.run()
