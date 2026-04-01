import datetime

def contains_right_income_statements(data : list[dict], date : datetime.datetime):
    return _contains_last_4_statements(data=data, date=date)

def contains_right_cashflow_statements(data : list[dict], date : datetime.datetime):
    return _contains_last_4_statements(data=data, date=date)

def _contains_last_4_statements(data : list[dict], date : datetime.datetime):
    if data is None:
        return False
    periods = set(p["period"] for p in data if p.get("period") in ("Q1", "Q2", "Q3", "Q4") )
    years= [y["calendarYear"] for y in data if y.get("calendarYear")] 
    if len(periods) < 4:
        return False
    if len(years) != len(data):
        return False
    if max(years) - min(years) > 1:
        return False
    if date.year - max(years) > 1:
        return False
    return True