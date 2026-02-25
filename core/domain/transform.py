def filter_rows_w_none(finance_data : list[dict]):
    return [dic for dic in finance_data if _contains_no_none(dic)]


def _contains_no_none(row : dict):
    for val in row.values():
        if val is None:
            return False
    return True
