from core.ports.base_repository_interface import BaseRepositoryInterface
from datetime import datetime
import pprint
from typing import Optional

class DashboardService():
    def __init__(self, finance_repo : BaseRepositoryInterface, company_repo : BaseRepositoryInterface) -> None:
        self.finance_repo = finance_repo
        self.company_repo= company_repo

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
    
    def get_distinct_company_data(self, key : str, filter : Optional[dict] = None):  
        result = self.company_repo.find_distinct(key = key, filter=filter)
        return result
    
    def get_company_suggestions(self, filter : Optional[dict] = None):  
        result = self.company_repo.find( filter=filter)
        return result
    def get_company_data(self, filter : Optional[dict] = None):  
        result = self.company_repo.find_one(filter=filter)
        return result
