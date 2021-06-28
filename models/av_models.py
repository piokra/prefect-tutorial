from datetime import datetime, timezone
from decimal import Decimal
from typing import Dict, List

from pydantic import BaseModel, Field


class InterdayMetaModel(BaseModel):
    information: str = Field(..., alias='1. Information')
    symbol: str = Field(..., alias='2. Symbol')
    last_refreshed: datetime = Field(..., alias="3. Last Refreshed")
    interval: str = Field(..., alias="4. Interval")
    output_size: str = Field(..., alias="5. Output Size")
    timezone: str = Field(..., alias="6. Time Zone")


class InterdayPointModel(BaseModel):
    open: Decimal = Field(..., alias="1. open")
    high: Decimal = Field(..., alias="2. high")
    low: Decimal = Field(..., alias="3. low")
    close: Decimal = Field(..., alias="4. close")
    volume: int = Field(..., alias="5. volume")


class InterdayResponseModel(BaseModel):
    meta: InterdayMetaModel = Field(..., alias="Meta Data")
    points: Dict[datetime, InterdayPointModel] = Field(..., alias="Time Series (15min)")


def interday_response_model_to_points(av_response_model: InterdayResponseModel,
                                      measurement='interday') -> List['influxdb_client.Point']:
    from influxdb_client import Point
    symbol = av_response_model.meta.symbol
    return [Point(measurement).tag('symbol', symbol)
                .field('open', value.open)
                .field('high', value.high)
                .field('low', value.low)
                .field('close', value.close)
                .field('volume', value.volume).time(key)
            for key, value in av_response_model.points.items()]
