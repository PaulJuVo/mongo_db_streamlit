from datetime import datetime
from core.domain.calculation import calc_mad, get_median_from_col, calc_robust_z_score, get_value_score, calc_momentum
from core.interfaces.base_repository_interface import BaseRepositoryInterface
from copy import copy
from infrastructure.mongo.mongo_connection import MongoConnection
from infrastructure.mongo.mongo_repository import MongoRepository
from config.mongo_config import MongoCollection, MongoDatabase, MongoUser
from dateutil.relativedelta import relativedelta

from app.shared.logging import init_logging
import logging
from config.logging_config import performance_log

init_logging()
logger = logging.getLogger("App - Ranking Service")

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
        self.ratios = ["psRatio", "pfcfRatio", "peRatio"]
        self.sector_data = [*self._get_sector_data()]
        self.sector_medians  = self._get_sector_median_data(self.sector_data)
        self.sector_mad= self._get_sector_mad(self.sector_data)
    @performance_log(logger)    
    def get_ranking(self):
        companies = self._get_companies()
        z_scores = [v + "_z_score" for v in self.ratios]
        columns = copy(self.ratios) 
        columns.extend(z_scores + ["symbol", "value_score", "momentum_score"])
        ranking : dict = {k : [] for k in columns}
        rows = []
        for company in companies:
            symbol = company["symbol"]
            median_data = self._get_company_median_data(symbol)
            z_scores = self._get_zscores(median_data)
            rows.append({
                "symbol": symbol,
                "value_score": get_value_score(z_scores),
                "momentum_score": self._get_momentum_score(symbol),
                **z_scores,
            })
        ranking = {k: [row.get(k) for row in rows] for k in columns}
        return ranking
        
    def _get_zscores(self, median_data : dict[str, float | None]):
        res = {}
        for k, v in median_data.items():
            mean = self.sector_medians[k]
            mad = self.sector_mad[k]
            if mean is not None and mad is not None and v is not None:
                res[k + "_z_score"] = calc_robust_z_score(v, mean, mad)
            else:
                res[k + "_z_score"] = None
        return res
    
    def _get_momentum_score(self, symbol):

        today = self.date
        six_m_ago = today - relativedelta(months=6)
        six_fiter = { "symbol": symbol, 
                                "date" : { 
                                    "$gte" : datetime(six_m_ago.year, six_m_ago.month, six_m_ago.day),
                                    }
                            }
        today_filter = { "symbol": symbol, 
                                "date" : { 
                                    "$lte": datetime(today.year, today.month, today.day)
                                    }
                            }
        start_rec = self.finance_repo.find_one(filter=six_fiter, sort={"date" : 1})
        end_rec = self.finance_repo.find_one(filter=today_filter, sort={"date" : -1})
        
        try:
            p_start = start_rec["adjClose"]
            p_end   = end_rec["adjClose"]
            return calc_momentum(p_end=p_end, p_start=p_start)
        except (TypeError, KeyError):
            pass
        return None

    def _get_companies(self):
        return [*self.company_repo.find(filter={"sector" : self.sector})]        

    def _get_sector_median_data(self, data):
        return dict({ratio : get_median_from_col(records=data, colname=ratio + "Median") for ratio in self.ratios})
    
    def _get_sector_mad(self, data):
        return dict({ratio : calc_mad(records=data, colname=ratio + "Median") for ratio in self.ratios})
    
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
    
    
