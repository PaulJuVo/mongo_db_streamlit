import pytest
from datetime import datetime

def test_create_finance_data_inserts_one_record(pipeline_service_finance):
    service, repos = pipeline_service_finance
    service.create_finance_data(b_size=100)

    inserted = repos["financedata_repo"].insert_many.call_args[0][0]
    assert len(inserted) == 1


def test_create_finance_data_pe_ratio(pipeline_service_finance):
    """PE = adjClose / eps_ttm  →  260.37 / (1.84+1.57+1.65+2.40) = 260.37 / 7.46 ≈ 34.9"""
    service, repos = pipeline_service_finance
    service.create_finance_data(b_size=100)

    record = repos["financedata_repo"].insert_many.call_args[0][0][0]
    assert record["peRatio"] == pytest.approx(260.37 / (1.84 + 1.57 + 1.65 + 2.40), rel=1e-3)


def test_create_finance_data_ps_ratio(pipeline_service_finance):
    """PS = adjClose / revenue_per_share_ttm"""
    avg_shares = (15150865000+15056133000+14948179000+15004697000) / 4
    rev_p_s_ttm=(124300000000+95359000000+94036000000+102456000000) / avg_shares
    exp_ps_ratio = 260.37 / rev_p_s_ttm 

    service, repos = pipeline_service_finance
    service.create_finance_data(b_size=100)

    record = repos["financedata_repo"].insert_many.call_args[0][0][0]
    assert record["psRatio"] is not None
    assert record["psRatio"] > 0
    assert record["psRatio"] == pytest.approx(exp_ps_ratio)


def test_create_finance_data_cashflow_ratios(pipeline_service_finance):
    avg_shares = (15150865000 + 15056133000 + 14948179000 + 15004697000) / 4
    fcf = 26486000000 + 24405000000 + 20881000000 + 26395000000
    ocf = 29745000000 + 27437000000 + 23452000000 + 29835000000
    ocf_p_s_ttm = ocf / avg_shares
    fcf_p_s_ttm = fcf / avg_shares
    exp_fcf_ratio = 260.37 / fcf_p_s_ttm 
    exp_ocf_ratio = 260.37 / ocf_p_s_ttm 

    service, repos = pipeline_service_finance
    service.create_finance_data(b_size=100)

    record = repos["financedata_repo"].insert_many.call_args[0][0][0]
    assert record["pfcfRatio"] is not None
    assert record["pfcfRatio"] == pytest.approx(exp_fcf_ratio)
    assert record["pcRatio"] is not None
    assert record["pcRatio"] == pytest.approx(exp_ocf_ratio)


def test_create_finance_data_symbol_and_date(pipeline_service_finance):
    service, repos = pipeline_service_finance
    service.create_finance_data(b_size=100)

    record = repos["financedata_repo"].insert_many.call_args[0][0][0]
    assert record["symbol"] == "AAPL"
    assert record["date"] == datetime(2026, 1, 9)
    assert record["adjClose"] == 260.37
