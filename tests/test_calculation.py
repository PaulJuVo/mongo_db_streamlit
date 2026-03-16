import core.domain.calculation as func
import pytest
from scipy.stats import median_abs_deviation

def test_sum_last_4(sample_staged_income_data):
    expected = 2.4 + 1.65 + 1.57 +  1.84
    assert func._sum_last_4(sample_staged_income_data, column_name="epsdiluted") == expected
    
    only_3 = [{"epsdiluted" : 1.0}, {"epsdiluted" : 1.0}, {"epsdiluted" : 1.0}]
    assert func._sum_last_4(only_3, column_name="epsdiluted") == None

def test_calc_ratio():
    assert func.calc_ratio(2, 1) == 0.5
    assert func.calc_ratio(0, 1) == 0
    assert func.calc_ratio(4, 3) == 0.75
    assert func.calc_ratio(10.0, 10.0) == 1.0

def test_get_median_from_col(sample_financedata, sample_financedata_only_none, sample_financedata_w_none):
    assert func.get_median_from_col(sample_financedata, colname="adjClose") == 3.02
    assert func.get_median_from_col(sample_financedata_only_none, colname="adjClose") == None
    assert func.get_median_from_col(sample_financedata_w_none, colname="adjClose") == 4.13

def test_get_cagr():
    assert func.calc_cagr(105, 100, 1) == 5.0
    assert func.calc_cagr(110, 100, 2) == 4.88
    assert func.calc_cagr(0, 100, 2) == -100.0
    with pytest.raises(ValueError):
        func.calc_cagr(10, 0, 2)
    with pytest.raises(ValueError):
        func.calc_cagr(10, 1, 0)
    with pytest.raises(ValueError):
        func.calc_cagr(-10, 10, 2)
    with pytest.raises(ValueError):
        func.calc_cagr(10, -1, 10)

def test_get_avg_shares(aapl_income):
    assert func.get_avg_shares(aapl_income) == pytest.approx((15004697000 + 14948179000 + 15056133000 + 15150865000) /4)

def test_calc_mad():
    records = [
        {"pe": 10.0},
        {"pe": None},
        {"pe": 14.0},
        {"pe": 16.0},
        {"pe": 18.0},
    ]
    assert func.calc_mad(records, "pe") == round(median_abs_deviation(sorted([10.0, 14.0, 16.0, 18.0])), 4)
    assert func.calc_mad([{"pe": None}, {"pe": None}], "pe") is None
    assert func.calc_mad([{"pe": 5.0}], "pe") == 0.0


def test_calc_robust_z_score():
    assert func.calc_robust_z_score(15.0, 10.0, 5.0) == pytest.approx(0.6745, rel=1e-3)
    assert func.calc_robust_z_score(10.0, 10.0, 5.0) == 0.0
    assert func.calc_robust_z_score(10.0, 10.0, 0.0) is None
    assert func.calc_robust_z_score(None, 10.0, 5.0) is None # type: ignore 
    assert func.calc_robust_z_score(10.0, None, 5.0) is None # type: ignore


def test_get_value_score():
    assert func.get_value_score({"pe": 1.0, "ps": 2.0, "pfcf": 3.0}) == -2.0
    assert func.get_value_score({"pe": -1.0, "ps": -2.0, "pfcf": -3.0}) == 2.0
    assert func.get_value_score({"pe": 1.0, "ps": None, "pfcf": None}) is None
    assert func.get_value_score({}) is None