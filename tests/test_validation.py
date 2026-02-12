import core.domain.validation as func

def test_is_income_statement_valid(sample_staged_income_data, 
                                   sample_income_period_w_duplicates,
                                   sample_income_period_w_none,
                                   sample_income_calyear_w_big_difference,
                                   sample_income_calyear_w_none,
                                   sample_income_date,
                                   sample_income_date_to_late):
    assert func.contains_right_income_statements(sample_staged_income_data,sample_income_date) == True
    assert func.contains_right_income_statements(sample_income_period_w_duplicates, sample_income_date) == False
    assert func.contains_right_income_statements(sample_income_period_w_none, sample_income_date) == False
    assert func.contains_right_income_statements(sample_income_calyear_w_none, sample_income_date) == False
    assert func.contains_right_income_statements(sample_income_calyear_w_big_difference, sample_income_date) == False
    assert func.contains_right_income_statements(sample_staged_income_data, sample_income_date_to_late) == False
