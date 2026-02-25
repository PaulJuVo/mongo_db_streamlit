

from typing import Optional

# TODO clean up 

def calc_ttm_eps(incom_stats : list[dict], column_name : str = "epsdiluted"):
    return _sum_last_4(stats=incom_stats, column_name=column_name)

def calc_revenue_per_share_ttm(incom_stats : list[dict], shares : Optional[float]):
    if shares is None:
        return None
    else:
        sum = _sum_last_4(stats=incom_stats, column_name="revenue")
        return sum / shares if sum and sum != 0 and shares != 0 else None

def calc_op_cashflow_per_share_ttm(cashflow_stats : list[dict], shares : Optional[float]):
    if shares is None:
        return None
    else:
        sum = _sum_last_4(stats=cashflow_stats, column_name="operatingCashFlow")
        return sum / shares if sum and sum != 0 and shares != 0 else None
    
def calc_free_cashflow_per_share_ttm(cashflow_stats : list[dict], shares : Optional[float]):
    if shares is None:
        return None
    else:
        sum = _sum_last_4(stats=cashflow_stats, column_name="freeCashFlow")
        return sum / shares if sum and sum != 0 and shares != 0 else None

def calc_pe_ratio(eps_ttm : Optional[float], adjclosed : float):
    if eps_ttm is None:
        return None
    if eps_ttm < 0:
        return None
    else:
        return adjclosed / eps_ttm if eps_ttm != 0 and adjclosed != 0 else 0

def calc_ps_ratio(rev_p_share_ttm : Optional[float], adjclosed : float):
    if rev_p_share_ttm is None:
        return None
    if rev_p_share_ttm < 0:
        return None
    else:
        return adjclosed / rev_p_share_ttm if rev_p_share_ttm != 0 and adjclosed != 0 else 0
    
def calc_pc_ratio(op_cashflow_ttm : Optional[float], adjclosed : float):
    if op_cashflow_ttm is None:
        return None
    if op_cashflow_ttm < 0:
        return None
    else:
        return adjclosed / op_cashflow_ttm if op_cashflow_ttm != 0 and adjclosed != 0 else 0
    
def calc_pfcf_ratio(free_cashflow_ttm : Optional[float], adjclosed : float):
    if free_cashflow_ttm is None:
        return None
    if free_cashflow_ttm < 0:
        return None
    else:
        return adjclosed / free_cashflow_ttm if free_cashflow_ttm != 0 and adjclosed != 0 else 0
    

def get_avg_shares(incom_stats : list[dict]):
    unpacked = [e["weightedAverageShsOutDil"] for e in incom_stats if e.get("weightedAverageShsOutDil") is not None]
    if len(unpacked) != 4:
        return None
    average = sum(unpacked) / 4
    return average


def _sum_last_4(stats : list[dict], column_name : str ):
    unpacked = [e[column_name] for e in stats if e.get(column_name) is not None]
    if len(unpacked) != 4:
        return None
    summed = sum(unpacked)
    return summed

