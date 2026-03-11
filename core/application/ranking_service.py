from datetime import datetime
from typing import Optional
from core.domain.calculation import calc_std, get_median_from_col, calc_z_score, get_value_score
from core.ports.base_repository_interface import BaseRepositoryInterface
from copy import copy
from infrastructure.mongo.mongo_connection import MongoConnection
from infrastructure.mongo.mongo_repository import MongoRepository
from config.mongo_config import MongoCollection, MongoDatabase, MongoUser


class RankingService():

    def __init__(self, 
                 finance_repo : BaseRepositoryInterface,
                 company_repo : BaseRepositoryInterface,
                 sector_repo : BaseRepositoryInterface,
                 date : datetime,
                 sector) -> None:
        self.finance_repo = finance_repo
        self.sector  = sector
        self.company_repo = company_repo
        self.sector_repo = sector_repo
        self.date = date
        self.ratios = ["psRatio", "pfcfRatio", "peRatio", "pcRatio"]
        self.sector_data = [*self._get_sector_data()]
        self.sector_medians  = self._get_sector_median_data(self.sector_data)
        self.sector_stds = self._get_sector_std(self.sector_data, self.sector_medians)
        
    def get_ranking(self):
        companies = self._get_companies()
        z_scores = [v + "_z_score" for v in self.ratios]
        columns = copy(self.ratios) 
        columns.extend(z_scores + ["symbol", "value_score"])
        ranking : dict = {k : [] for k in columns}
        rows = []
        for company in companies:
            symbol = company["symbol"]
            median_data = self._get_company_median_data(symbol)
            z_scores = self._get_zscores(median_data)
            rows.append({
                "symbol": symbol,
                "value_score": get_value_score(z_scores),
                **median_data,
                **z_scores,
            })
        ranking = {k: [row.get(k) for row in rows] for k in columns}
        return ranking
        
    def _get_zscores(self, median_data : dict[str, float | None]):
        res = {}
        for k, v in median_data.items():
            mean = self.sector_medians[k]
            std = self.sector_stds[k]
            if mean is not None and std is not None and v is not None:
                res[k + "_z_score"] = calc_z_score(v, mean, std)
            else:
                res[k + "_z_score"] = None
        return res

    def _get_companies(self):
        return [*self.company_repo.find(filter={"sector" : self.sector})]        

    def _get_sector_median_data(self, data):
        return dict({ratio : get_median_from_col(records=data, colname=ratio + "Median") for ratio in self.ratios})
    
    def _get_sector_std(self, data, medians : dict):
        return dict({ratio : calc_std(records=data, colname=ratio + "Median", mean=medians[ratio]) for ratio in self.ratios})
    
    def _get_company_median_data(self, symbol):
        date1 = self.date
        fi = { "symbol": symbol, 
                                "date" : { 
                                    "$gte" : datetime(date1.year - 1, date1.month, date1.day),
                                    "$lte": datetime(date1.year, date1.month, date1.day)
                                    }
                            }
        result = self.finance_repo.find(filter=fi)
        lis = [*result]
        ret = {ratio : get_median_from_col(records=lis, colname=ratio) for ratio in self.ratios}
        return ret
    
    def _get_sector_data(self):
        date1 = self.date
        fi = { "sector": self.sector, 
                                "date" : { 
                                    "$gte" : datetime(date1.year - 1, date1.month, date1.day),
                                    "$lte": datetime(date1.year, date1.month, date1.day)
                                    }
                            }
        return self.sector_repo.find(filter=fi)
    
    


if __name__ == "__main__":
    import pandas as pd
    with MongoConnection(MongoUser.APPUSER) as conn:
        fin = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.FINANCEDATA)
        sec = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.SECTORDATA)
        com = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.COMPANYDATA)
        date = datetime(2025,12,28)
        sector = "Technology"
        service = RankingService(fin,com, sec, date, sector)
        ranking = service.get_ranking()
        df = pd.DataFrame(ranking)
        #print(df)
