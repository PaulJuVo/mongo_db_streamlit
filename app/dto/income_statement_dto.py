from pydantic import HttpUrl, Field
from app.dto.base_dto import BaseDto
from datetime import date
from typing import Optional

class IncomeStatementDto(BaseDto):
    date: date
    symbol: Optional[str] = None

    reported_currency: Optional[str] = Field(
        default=None, alias="reportedCurrency"
    )
    calendar_year: Optional[str] = Field(
        default=None, alias="calendarYear"
    )

    revenue: Optional[float] = None
    cost_of_revenue: Optional[float] = Field(
        default=None, alias="costOfRevenue"
    )

    gross_profit: Optional[float] = Field(
        default=None, alias="grossProfit"
    )
    gross_profit_ratio: Optional[float] = Field(
        default=None, alias="grossProfitRatio"
    )

    research_and_development_expenses: Optional[float] = Field(
        default=None, alias="researchAndDevelopmentExpenses"
    )

    selling_general_and_administrative_expenses: Optional[float] = Field(
        default=None, alias="sellingGeneralAndAdministrativeExpenses"
    )

    operating_expenses: Optional[float] = Field(
        default=None, alias="operatingExpenses"
    )

    ebitda: Optional[float] = None
    ebitda_ratio: Optional[float] = Field(
        default=None, alias="ebitdaRatio"
    )

    operating_income: Optional[float] = Field(
        default=None, alias="operatingIncome"
    )
    operating_income_ratio: Optional[float] = Field(
        default=None, alias="operatingIncomeRatio"
    )

    income_before_tax: Optional[float] = Field(
        default=None, alias="incomeBeforeTax"
    )
    income_before_tax_ratio: Optional[float] = Field(
        default=None, alias="incomeBeforeTaxRatio"
    )

    income_tax_expense: Optional[float] = Field(
        default=None, alias="incomeTaxExpense"
    )

    net_income: Optional[float] = Field(
        default=None, alias="netIncome"
    )
    net_income_ratio: Optional[float] = Field(
        default=None, alias="netIncomeRatio"
    )

    eps: Optional[float] = None
    eps_diluted: Optional[float] = Field(
        default=None, alias="epsdiluted"
    )

    weighted_average_shs_out: Optional[float] = Field(
        default=None, alias="weightedAverageShsOut"
    )
    weighted_average_shs_out_dil: Optional[float] = Field(
        default=None, alias="weightedAverageShsOutDil"
    )

    final_link: Optional[HttpUrl] = Field(
        default=None, alias="finalLink"
    )