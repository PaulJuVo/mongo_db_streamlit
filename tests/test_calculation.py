import core.domain.calculation as func
import pytest

def test_calc_ttm_eps(sample_staged_income_data):
    expected = 2.4 + 1.65 + 1.57 +  1.84
    assert func.calc_ttm_eps(sample_staged_income_data) == expected
    
    only_3 = [{"epsdiluted" : 1.0}, {"epsdiluted" : 1.0}, {"epsdiluted" : 1.0}]
    with pytest.raises(Exception) as e_info:
        func.calc_ttm_eps(only_3)

def test_calc_pe_ratio():
    assert func.calc_pe_ratio(2, 1) == 0.5
    assert func.calc_pe_ratio(0, 1) == 0
    assert func.calc_pe_ratio(4, 3) == 0.75
    assert func.calc_pe_ratio(10.0, 10.0) == 1.0

    

    