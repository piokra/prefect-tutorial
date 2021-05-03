from datetime import timedelta

import prefect
from prefect import task, Flow, Parameter
from prefect.schedules import IntervalSchedule
from prefect.storage import GitHub

from alpha_vantage.timeseries import TimeSeries


@task
def scrap_stock(stock: str):
    logger = prefect.context.get("logger")
    logger.info(f"Scrapping {stock}!")
    ts = TimeSeries(key='KEY')
    # Get json object with the intraday data and another with  the call's metadata
    data, meta_data = ts.get_intraday('GOOGL')
    logger.info(data)
    logger.info(meta_data)


schedule = IntervalSchedule(interval=timedelta(minutes=2))

with Flow("scrap-stock", schedule) as flow:
    stocks = Parameter("stocks", default=["GOOGL", "MSFT"])
    scrap_stock.map(stocks)

flow.storage = GitHub(
    repo="piokra/prefect-tutorial",
    path="scrap-stock.py"
)

flow.run()
