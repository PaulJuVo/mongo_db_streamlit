import pytest
from datetime import datetime, date
from unittest.mock import MagicMock, patch
from core.application.pipeline_service import PipelineService
from core.interfaces.base_repository_interface import BaseRepositoryInterface
from tests.data.example_data import APPLE_CORRECT, APPLE_ONLY_NONE, APPLE_W_NONE

@pytest.fixture
def sample_staged_income_data():
    test_data = [{'_id': '698caa0868736367c3c3d965', 'symbol': 'AAPL', 'period': 'Q4', 'eps': 1.85, 'epsdiluted': 1.84, 'date': datetime(2025, 9, 27, 0, 0), 'fillingDate': datetime(2025, 10, 31, 0, 0), 'calendarYear': 2025},
{'_id': '698caa0868736367c3c3d966', 'symbol': 'AAPL', 'period': 'Q3', 'eps': 1.57, 'epsdiluted': 1.57, 'date': datetime(2025, 6, 28, 0, 0), 'fillingDate': datetime(2025, 8, 1, 0, 0), 'calendarYear': 2025},
{'_id': '698caa0868736367c3c3d967', 'symbol': 'AAPL', 'period': 'Q2', 'eps': 1.65, 'epsdiluted': 1.65, 'date': datetime(2025, 3, 29, 0, 0), 'fillingDate': datetime(2025, 5, 2, 0, 0), 'calendarYear': 2025},
{'_id': '698caa0868736367c3c3d968', 'symbol': 'AAPL', 'period': 'Q1', 'eps': 2.41, 'epsdiluted': 2.4, 'date': datetime(2024, 12, 28, 0, 0), 'fillingDate': datetime(2025, 1, 31, 0, 0), 'calendarYear': 2025}]

    return test_data

@pytest.fixture
def sample_income_period_w_duplicates():
    test_data = [{'calendarYear': 2025, 'period': 'Q4'},{'calendarYear': 2025,'period': 'Q3'},{'calendarYear': 2025,'period': 'Q2'},{'calendarYear': 2025,'period': 'Q4'}]
    return test_data

@pytest.fixture
def sample_income_period_w_none():
    test_data = [{'calendarYear': 2025, 'period': 'Q4'},{'calendarYear': 2025,'period': 'Q3'},{'calendarYear': 2025,'period': 'Q2'},{'calendarYear': 2025, 'period': None}]
    return test_data

@pytest.fixture
def sample_income_calyear_w_big_difference():
    test_data = [{'calendarYear': 2025, 'period': 'Q4'},{'calendarYear': 2025,'period': 'Q3'},{'calendarYear': 2025,'period': 'Q2'},{'calendarYear': 2023,'period': 'Q1'}]
    return test_data

@pytest.fixture
def sample_income_calyear_w_none():
    test_data = [{'calendarYear': 2025, 'period': 'Q4'},{'calendarYear': 2025,'period': 'Q3'},{'calendarYear': 2025,'period': 'Q2'},{'calendarYear': None, 'period': "Q1"}]
    return test_data

@pytest.fixture
def sample_income_date():
    return date(2026, 1, 1)

@pytest.fixture
def sample_income_date_to_late():
    return date(2027, 1, 1)

@pytest.fixture
def sample_financedata():
    return APPLE_CORRECT

@pytest.fixture
def sample_financedata_w_none():
    return APPLE_W_NONE

@pytest.fixture
def sample_financedata_only_none():
    return APPLE_ONLY_NONE




@pytest.fixture
def mock_repos():
    repo_names = [
        "eodprice_repo", "income_repo", "cashflow_repo",
        "staged_eodprice_repo", "staged_income_repo", "staged_cashflow_repo",
        "profile_repo", "financedata_repo", "company_repo",
        "constituents_repo", "scd_constituents_repo", "sector_repo",
        "sp500_raw_repo", "sp500_repo",
    ]
    return {name: MagicMock(spec=BaseRepositoryInterface) for name in repo_names}


### Following Data is not real


@pytest.fixture
def aapl_eod():
    return [
        {
            "_id": "699f172f47d6253856785b05",
            "symbol": "AAPL",
            "date": datetime(2026, 1, 9),
            "adjClose": 260.37
        }
    ]

@pytest.fixture
def aapl_income():
    return [
        {
            "symbol": "AAPL", "period": "Q4",
            "revenue": 102456000000,
            "eps": 1.75, "epsdiluted": 1.74,
            "weightedAverageShsOutDil": 15004697000,
            "date": datetime(2025, 9, 27),
            "fillingDate": datetime(2025, 10, 31),
            "calendarYear": 2025,
        },
        {
            "symbol": "AAPL", "period": "Q3",
            "revenue": 94036000000,
            "eps": 1.67, "epsdiluted": 1.67,
            "weightedAverageShsOutDil": 14948179000,
            "date": datetime(2025, 6, 28),
            "fillingDate": datetime(2025, 8, 1),
            "calendarYear": 2025,
        },
        {
            "symbol": "AAPL", "period": "Q2",
            "revenue": 95359000000,
            "eps": 1.75, "epsdiluted": 1.75,
            "weightedAverageShsOutDil": 15056133000,
            "date": datetime(2025, 3, 29),
            "fillingDate": datetime(2025, 5, 2),
            "calendarYear": 2025,
        },
        {
            "symbol": "AAPL", "period": "Q1",
            "revenue": 124300000000,
            "eps": 2.31, "epsdiluted": 2.30,
            "weightedAverageShsOutDil": 15150865000,
            "date": datetime(2024, 12, 28),
            "fillingDate": datetime(2025, 1, 31),
            "calendarYear": 2025,
        },
    ]



@pytest.fixture
def aapl_cashflow():
    return [
        {
            "symbol": "AAPL", "period": "Q4",
            "operatingCashFlow": 29745000000,
            "freeCashFlow": 26486000000,
            "date": datetime(2025, 9, 27),
            "fillingDate": datetime(2025, 10, 31),
            "calendarYear": 2025,
        },
        {
            "symbol": "AAPL", "period": "Q3",
            "operatingCashFlow": 27437000000,
            "freeCashFlow": 24405000000,
            "date": datetime(2025, 6, 28),
            "fillingDate": datetime(2025, 8, 1),
            "calendarYear": 2025,
        },
        {
            "symbol": "AAPL", "period": "Q2",
            "operatingCashFlow": 23452000000,
            "freeCashFlow": 20881000000,
            "date": datetime(2025, 3, 29),
            "fillingDate": datetime(2025, 5, 2),
            "calendarYear": 2025,
        },
        {
            "symbol": "AAPL", "period": "Q1",
            "operatingCashFlow": 29835000000,
            "freeCashFlow": 26395000000,
            "date": datetime(2024, 12, 28),
            "fillingDate": datetime(2025, 1, 31),
            "calendarYear": 2025,
        },
    ]

@pytest.fixture
def pipeline_service(mock_repos):
    return PipelineService(**mock_repos)

@pytest.fixture
def pipeline_service_finance(mock_repos, aapl_eod, aapl_income, aapl_cashflow):
    mock_repos["staged_eodprice_repo"].find.return_value = iter(aapl_eod)
    mock_repos["staged_income_repo"].find.return_value = iter(aapl_income)
    mock_repos["staged_cashflow_repo"].find.return_value = iter(aapl_cashflow)
    return PipelineService(**mock_repos), mock_repos

