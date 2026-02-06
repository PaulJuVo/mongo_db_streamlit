from pydantic import Field
from app.dto.base_dto import BaseDto
from datetime import date
from typing import Optional

class EodPricesDTO(BaseDto):
    symbol: str
    date: date

    open: float
    high: float
    low: float
    close: float

    adj_close: Optional[float] = Field(default=None, alias="adjClose")
    volume: Optional[int] = None
    unadjusted_volume: Optional[int] = Field(
        default=None,
        alias="unadjustedVolume"
    )

    change: Optional[float] = None
    change_percent: Optional[float] = Field(
        default=None,
        alias="changePercent"
    )

    vwap: Optional[float] = None
    label: Optional[str] = None

    change_over_time: Optional[float] = Field(
        default=None,
        alias="changeOverTime"
    )