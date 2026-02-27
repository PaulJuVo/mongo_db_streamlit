from core.ports.base_repository_interface import BaseRepositoryInterface
from datetime import datetime, date
from statistics import median
from itertools import filterfalse
from math import isnan
from typing import Optional

class DashboardService():
    def __init__(self, 
                finance_repo : BaseRepositoryInterface, 
                company_repo : BaseRepositoryInterface,
                sector_repo : BaseRepositoryInterface,
                sp_500_repo : BaseRepositoryInterface) -> None:
        self.finance_repo = finance_repo
        self.company_repo= company_repo
        self.sector_repo = sector_repo
        self.sp_500_repo = sp_500_repo


    def get_finance_data(self, companies : list, from_date : datetime, to_date : datetime, projection : list):

        fi = { "symbol": { 
                                    "$in": companies
                                    }, 
                                "date" : { 
                                    "$gte" : from_date,
                                    "$lte" : to_date
                                    }
                            }
        
        proj = {"_id" : 0}
        proj.update({k : 1 for k in projection})
        
        result = self.finance_repo.find(filter=fi, projection=proj)
        res_list = [*result]
        if not res_list:
            # TODO throw own exception
            raise ValueError()
        else: 
            return res_list
        
    def get_sp500_data(self, index, from_date : datetime, to_date : datetime):
        fi = { "symbol": index, 
                                "date" : { 
                                    "$gte" : from_date,
                                    "$lte" : to_date
                                    }
                            }
        result = self.sp_500_repo.find(filter=fi)
        res_list = [*result]
        if not res_list:
            # TODO throw own exception
            raise ValueError()
        else: 
            return res_list
    
    def get_distinct_company_data(self, key : str, filter : Optional[dict] = None):  
        result = self.company_repo.find_distinct(key = key, filter=filter)
        return result
    
    def get_company_suggestions(self, filter : Optional[dict] = None):  
        result = self.company_repo.find( filter=filter)
        return result
    def get_company_data(self, filter : Optional[dict] = None):  
        result = self.company_repo.find_one(filter=filter)
        return result
    
    def get_sector_median_data(self, sector, ratio, date1 : datetime):
        result = self.sector_repo.find(filter={"sector": sector,"date" : { "$gte" : datetime(date1.year - 1, date1.month, date1.day), "$lte" : date1}})
        clean = list([v[ratio] for v in result if v[ratio] is not None ])
        last_year = round(median(sorted(clean)),2)

        result = self.sector_repo.find(filter={"sector": sector, "date" : { "$gte" : datetime(date1.year - 5, date1.month, date1.day), "$lte" : date1}})
        clean = list([v[ratio] for v in result if v[ratio] is not None ])
        five_year = round(median(sorted(clean)),2)

        result = self.sector_repo.find(filter={"sector": sector, "date" : { "$gte" : datetime(date1.year - 10, date1.month, date1.day), "$lte" : date1}})
        clean = list([v[ratio] for v in result if v[ratio] is not None ])
        ten_year = round(median(sorted(clean)),2)

        return last_year, five_year, ten_year

