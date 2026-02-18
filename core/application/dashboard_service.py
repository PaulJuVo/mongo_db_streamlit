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



if __name__ == "__main__":
    from infrastructure.mongo.mongo_repository import MongoRepository
    from infrastructure.mongo.mongo_connection import MongoConnection
    from config.mongo_config import MongoCollection, MongoDatabase, MongoUser
    from core.application.dashboard_service import DashboardService
    from datetime import datetime
    with MongoConnection(MongoUser.DASHBOARDUSER) as conn:
        finance_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.FINANCEDATA)
        company_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.COMPANYDATA)
        dashboard_service = DashboardService(finance_repo=finance_repo, company_repo=company_repo)
        

        df_ts = dashboard_service.get_finance_data(companies=["AAPL", "A"], 
                                       from_date=datetime(2010, 1, 1), 
                                       to_date=datetime(2010, 1, 10),
                                       projection=["date", "symbol", "peRatio"])

        pprint.pprint(df_ts)