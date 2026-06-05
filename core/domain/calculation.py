from statistics import median
from scipy.stats import median_abs_deviation
from typing import Optional

def calc_ttm_eps(incom_stats : list[dict], column_name : str = "epsdiluted"):
    return _sum_last_4(stats=incom_stats, column_name=column_name)

def calc_per_share_ttm(stats : list[dict], shares : Optional[float], colname : str):
    if shares is None:
        return None
    else:
        sum = _sum_last_4(stats=stats, column_name=colname)
        return sum / shares if sum and sum != 0 and shares != 0 else None

def calc_ratio(ttm: Optional[float], adjclosed: float):
    if ttm is None or ttm <= 0:
        return None
    if abs(ttm) < 0.01:   # TTM zu klein → PE wäre unrealistisch
        return None
    return adjclosed / ttm if adjclosed != 0 else None 

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

def get_median_from_col(records : list[dict], colname):
    clean = list([v[colname] for v in records if v[colname] is not None])
    if clean:
        return float(round(median(sorted(clean)),4))
    else:
        return None

def calc_cagr(end_value : float, beginning_value : float, number_of_years : int):
    if any(v is None for v in (end_value, beginning_value, number_of_years)):
        raise ValueError()
    if beginning_value == 0 or number_of_years < 1:
        raise ValueError()
    if beginning_value < 0 or end_value < 0:
        raise ValueError()
    cagr : float = (pow(end_value/beginning_value, (1/number_of_years)) - 1 ) * 100
    return round(cagr,2)

def calc_mad(records : list[dict], colname):
    clean = list([v[colname] for v in records if v[colname] is not None])
    if clean:
        return round(median_abs_deviation(sorted(clean)),4)
    else:
        return None
    
def calc_robust_z_score(value : float, mean : float, mad : float):
    if any(v is None for v in (value, mean, mad)):
        return None
    return 0.6745 * ((value - mean) / mad) if mad != 0 else None

def get_value_score(z_scores : dict):
    scores = [sc for sc in z_scores.values() if sc is not None]
    if len(scores) < 3:
        return None
    return float(round(median(scores), 2)) * -1

def calc_momentum(p_start, p_end):
    if p_start and p_end and p_start > 0:
        return (p_end - p_start) / p_start
