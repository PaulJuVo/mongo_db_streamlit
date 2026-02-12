

def calc_ttm_eps(incom_stats : list[dict], column_name : str = "epsdiluted"):
    unpacked = [e[column_name] for e in incom_stats if e.get(column_name) is not None]
    # eigentlich unmöglich, da bei schema geprüft wird
    if len(unpacked) != 4:
        raise ValueError(f"{column_name} does not contain 4 values to calculate ttm eps")
    ttm_eps = sum(unpacked)
    return ttm_eps

def calc_pe_ratio(eps_ttm : float, adjclosed : float):
    return adjclosed / eps_ttm if eps_ttm != 0 and adjclosed != 0 else 0