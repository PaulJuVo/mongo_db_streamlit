from pydantic import HttpUrl, Field
from app.dto.base_dto import BaseDto
from typing import Optional
from datetime import date

class ProfileDto(BaseDto):
    symbol: str

    company_name: Optional[str] = Field(default=None, alias="companyName")
    price: float

    beta: Optional[float] = None
    vol_avg: Optional[float] = Field(default=None, alias="volAvg")
    mkt_cap: Optional[float] = Field(default=None, alias="mktCap")
    last_div: Optional[float] = Field(default=None, alias="lastDiv")
    changes: Optional[float] = None

    currency: str
    exchange: str

    industry: Optional[str] = None
    website: Optional[HttpUrl] = None
    description: Optional[str] = None
    ceo: Optional[str] = None
    sector: Optional[str] = None
    country: Optional[str] = None

    full_time_employees: Optional[int] = Field(default=None, alias="fullTimeEmployees")
    city: Optional[str] = None
    state: Optional[str] = None
    ipo_date: Optional[date] = Field(default=None, alias="ipoDate")

    image: Optional[HttpUrl] = None

    is_actively_trading: bool = Field(alias="isActivelyTrading")
    is_etf: bool = Field(alias="isEtf")