import core.domain.calculation as func
import pytest

def test_calc_ttm_eps(sample_staged_income_data):
    expected = 2.4 + 1.65 + 1.57 +  1.84
    assert func.calc_ttm_eps(sample_staged_income_data) == expected
    
    only_3 = [{"epsdiluted" : 1.0}, {"epsdiluted" : 1.0}, {"epsdiluted" : 1.0}]
    assert func.calc_ttm_eps(only_3) == None

def test_calc_pe_ratio():
    assert func.calc_pe_ratio(2, 1) == 0.5
    assert func.calc_pe_ratio(0, 1) == 0
    assert func.calc_pe_ratio(4, 3) == 0.75
    assert func.calc_pe_ratio(10.0, 10.0) == 1.0

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
    

    