import pytest
import datetime
from tests.data.example_data import APPLE_CORRECT, APPLE_ONLY_NONE, APPLE_W_NONE

@pytest.fixture
def sample_staged_income_data():
    test_data = [{'_id': '698caa0868736367c3c3d965', 'symbol': 'AAPL', 'period': 'Q4', 'eps': 1.85, 'epsdiluted': 1.84, 'date': datetime.datetime(2025, 9, 27, 0, 0), 'fillingDate': datetime.datetime(2025, 10, 31, 0, 0), 'calendarYear': 2025},
{'_id': '698caa0868736367c3c3d966', 'symbol': 'AAPL', 'period': 'Q3', 'eps': 1.57, 'epsdiluted': 1.57, 'date': datetime.datetime(2025, 6, 28, 0, 0), 'fillingDate': datetime.datetime(2025, 8, 1, 0, 0), 'calendarYear': 2025},
{'_id': '698caa0868736367c3c3d967', 'symbol': 'AAPL', 'period': 'Q2', 'eps': 1.65, 'epsdiluted': 1.65, 'date': datetime.datetime(2025, 3, 29, 0, 0), 'fillingDate': datetime.datetime(2025, 5, 2, 0, 0), 'calendarYear': 2025},
{'_id': '698caa0868736367c3c3d968', 'symbol': 'AAPL', 'period': 'Q1', 'eps': 2.41, 'epsdiluted': 2.4, 'date': datetime.datetime(2024, 12, 28, 0, 0), 'fillingDate': datetime.datetime(2025, 1, 31, 0, 0), 'calendarYear': 2025}]

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
    return datetime.date(2026, 1, 1)

@pytest.fixture
def sample_income_date_to_late():
    return datetime.date(2027, 1, 1)

@pytest.fixture
def sample_financedata():
    return APPLE_CORRECT

@pytest.fixture
def sample_financedata_w_none():
    return APPLE_W_NONE

@pytest.fixture
def sample_financedata_only_none():
    return APPLE_ONLY_NONE