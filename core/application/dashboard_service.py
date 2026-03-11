from core.ports.base_repository_interface import BaseRepositoryInterface
from core.domain.calculation import get_median_from_col, calc_cagr
from core.exceptions.dashboard_exceptions import NoDataFound
from datetime import datetime
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
            raise NoDataFound(message=f"No data found for filter = {fi}", errorcode=999)
        else: 
            return res_list
    def get_data_edge(self):
        result = self.finance_repo.find_one(sort={"date" : -1})
        return result["date"]

        
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
            raise NoDataFound(message=f"No data found for filter = {fi}", errorcode=999)
        else: 
            return res_list
    
    def get_distinct_company_data(self, key : str, filter : Optional[dict] = None):  
        result = self.company_repo.find_distinct(key = key, filter=filter)
        return result
    
    def get_company_suggestions(self, filter : Optional[dict] = None):  
        result = self.company_repo.find( filter=filter, sort={"symbol": 1})
        return result
    
    def get_company_data(self, filter : Optional[dict] = None):  
        result = self.company_repo.find_one(filter=filter)
        return result
    
    def get_all_company_data(self, filter : Optional[dict] = None):  
        result = self.company_repo.find(filter=filter)
        return result
    
    def get_sector_median_data_last_years(self, sector, ratio, date1 : datetime):
        last_year = self.get_sector_median_data(sector=sector,ratio=ratio, from_date=datetime(date1.year - 1, date1.month, date1.day), to_date=date1)
        five_year = self.get_sector_median_data(sector=sector,ratio=ratio, from_date=datetime(date1.year - 5, date1.month, date1.day), to_date=date1)
        ten_year = self.get_sector_median_data(sector=sector,ratio=ratio, from_date=datetime(date1.year - 10, date1.month, date1.day), to_date=date1)
        return last_year, five_year, ten_year
    
    def get_company_median_data(self, symbol, ratio, from_date : datetime, to_date : datetime):
        fi = { "symbol": symbol, 
                                "date" : { 
                                    "$gte" : from_date,
                                    "$lte" : to_date
                                    }
                            }
        projection={"date" : 1, ratio : 1, "_id" : 0}
        
        result = self.finance_repo.find(filter=fi, projection=projection)
        return get_median_from_col(records=[*result], colname=ratio)
    

    def get_sector_median_data(self, sector, ratio, from_date : datetime, to_date : datetime):
        fi = { "sector": sector, 
                                "date" : { 
                                    "$gte" : from_date,
                                    "$lte" : to_date
                                    }
                            }
        projection={"date" : 1, ratio : 1, "_id" : 0}
        
        result = self.sector_repo.find(filter=fi, projection=projection)
        return get_median_from_col(records=[*result], colname=ratio)
        
    
    def map_symbol_to_sector(self, symbol):
        res = self.company_repo.find_one(filter={"symbol" : symbol})
        return res["sector"] if res is not None else None
    
    def get_cagr(self, repo : BaseRepositoryInterface, symbol, date1 : datetime, number_of_years : int, forward : bool = False):
        if forward:
            start_date = datetime(date1.year, date1.month, date1.day)
            end_date = datetime(date1.year + number_of_years, date1.month, date1.day)
        else:
            start_date = datetime(date1.year - number_of_years, date1.month, date1.day)
            end_date = datetime(date1.year, date1.month, date1.day)
            
        end_rec = repo.find_one(
            {
                "symbol": symbol,
                "date": {
                    "$lte": end_date
                },
            },
            sort={"date": -1}
        )
        beginning_rec = repo.find_one(
            {
                "symbol": symbol,
                "date": {
                    "$gte": start_date
                },
            },
            sort={"date": 1}
        )
        if end_rec is None or beginning_rec is None:
            raise NoDataFound("Couldn't calculate: Either end or beginning records are None", None)
        return calc_cagr(end_value=end_rec["adjClose"], beginning_value=beginning_rec["adjClose"], number_of_years=number_of_years)


    def get_financedata_cagr(self, symbol, date1 : datetime, number_of_years : int, forward : bool = False):
        return self.get_cagr(self.finance_repo, symbol, date1, number_of_years, forward)
    
    def get_sp500data_cagr(self, symbol, date1 : datetime, number_of_years : int, forward : bool = False):
        return self.get_cagr(self.sp_500_repo, symbol, date1, number_of_years, forward)
    

        



