from influxdb import DataFrameClient
from injector import Injector
from prefect import task


@task
def load_df_to_influx_task(dataframe: 'DataFrame', measurement: str, injector: Injector):
    df_client = injector.get(DataFrameClient)

    df_client.write_points(dataframe, measurement)
