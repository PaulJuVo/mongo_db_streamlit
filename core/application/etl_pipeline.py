
from core.ports.base_repository_interface import BaseRepositoryInterface
from config.logging_config import performance_log
from config.mongo_config import FINANCEDATA_TIMESERIES_CONFIG
from config.pipeline_config import COMPANY_PIPELINE, INCOME_STAGED, EOD_STAGED
from core.domain.validation import contains_right_income_statements
from core.domain.calculation import calc_ttm_eps, calc_pe_ratio, calc_ttm_net_income
from collections import defaultdict
import logging
import pprint

logger = logging.getLogger(__name__)

class PipelineService:
    def __init__(self, 
                 eodprice_repo : BaseRepositoryInterface, 
                 income_repo : BaseRepositoryInterface,
                 staged_eodprice_repo : BaseRepositoryInterface, 
                 staged_income_repo : BaseRepositoryInterface,
                 profile_repo : BaseRepositoryInterface,
                 financedata_repo : BaseRepositoryInterface,
                 company_repo : BaseRepositoryInterface
                 ):
        self.eodprice_repo = eodprice_repo
        self.income_repo = income_repo
        self.staged_eodprice_repo = staged_eodprice_repo
        self.staged_income_repo = staged_income_repo
        self.profile_repo = profile_repo
        self.financedata_repo = financedata_repo
        self.company_repo = company_repo

    def run(self):
        self.upsert_company_data()
        #self.upsert_eod_staged()
        #self.upsert_income_staged()
        #self.create_finance_data(2000)


        
    @performance_log(logger)
    def create_finance_data(self, b_size):
        results = self.staged_eodprice_repo.find(batch_size=b_size)
        to_copy = ["date", "adjClose", "symbol", "unadjustedVolume"]
        processed_data = []

        self.financedata_repo.drop()
        self.financedata_repo.create_time_series(config=FINANCEDATA_TIMESERIES_CONFIG)

        for eod_price in results:
            finance_data = {k: v for k, v in eod_price.items() if k in to_copy}
            date = eod_price["date"]
            symbol = eod_price["symbol"]

            income_cursor = self.staged_income_repo.find(filter={"symbol": symbol, "fillingDate" : { "$lte" : date}}, limit=4)
            incom_stats = [*income_cursor]

            if contains_right_income_statements(incom_stats, eod_price["date"]):
                eps_ttm = calc_ttm_eps(incom_stats)
                adjclosed = eod_price["adjClose"]
                finance_data["peRatio"] = calc_pe_ratio(eps_ttm, adjclosed)
                finance_data["eps_diluted_ttm"] = eps_ttm
                finance_data["net_income_ttm"] = calc_ttm_net_income(incom_stats)
            else:    
                finance_data["peRatio"] = None
                finance_data["eps_diluted_ttm"] = None
                finance_data["net_income_ttm"] = None

            processed_data.append(finance_data)
        self.financedata_repo.insert_many(processed_data)

    def upsert_company_data(self):
        self.company_repo.create_index(keys=[("symbol", 1)], unique=True)
        self.profile_repo.execute_pipeline(COMPANY_PIPELINE)

    def upsert_eod_staged(self):
        self.staged_eodprice_repo.create_index(keys=[("symbol", 1), ("date", -1)], unique=True)
        self.eodprice_repo.execute_pipeline(EOD_STAGED)

    def upsert_income_staged(self):
        self.staged_income_repo.create_index(keys=[("symbol", 1), ("date", -1)], unique=True)
        self.income_repo.execute_pipeline(INCOME_STAGED)
        self.staged_income_repo.create_index(keys=[("symbol", 1), ("fillingDate", -1)], unique=False)

        


if __name__ == "__main__":
    from infrastructure.mongo.mongo_repository import MongoRepository
    from infrastructure.mongo.mongo_connection import MongoConnection
    from config.mongo_config import MongoCollection, MongoDatabase, MongoUser
    with MongoConnection(MongoUser.DASHBOARDUSER) as conn:
        finance_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.FINANCEDATA)
        company_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.COMPANYDATA)
        eod_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.EODPRICE)
        staged_eod_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.STAGED_EODPRICE)
        staged_income_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.STAGED_INCOMESTATEMENT)
        income_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.INCOMESTATEMENT)
        profile_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.PROFILE)
        pipeline_service = PipelineService(eodprice_repo=eod_repo, 
                                            income_repo=income_repo, 
                                            staged_eodprice_repo=staged_eod_repo, 
                                            staged_income_repo=staged_income_repo, 
                                            profile_repo=profile_repo, 
                                            financedata_repo=finance_repo, 
                                            company_repo=company_repo)
        
        
