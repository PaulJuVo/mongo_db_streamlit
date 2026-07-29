from core.interfaces.base_repository_interface import BaseRepositoryInterface
from core.domain.calculation import get_median_from_col, calc_cagr
from core.exceptions.dashboard_exceptions import NoDataFound
from core.application.ranking_service import RankingService
from core.application.dashboard_service import DashboardService
from core.domain.calculation import calc_cagr
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Optional
import logging
from config.logging_config import performance_log
import pandas as pd

logger = logging.getLogger("Notebook Service")


class NotebookService():
    def __init__(self, 
                finance_repo : BaseRepositoryInterface, 
                company_repo : BaseRepositoryInterface,
                sector_repo : BaseRepositoryInterface,
                sp_500_repo : BaseRepositoryInterface,
                constituents_repo : BaseRepositoryInterface) -> None:
        self.finance_repo = finance_repo
        self.company_repo= company_repo
        self.sector_repo = sector_repo
        self.sp_500_repo = sp_500_repo
        self.constituents_repo = constituents_repo
        self.dashboard_service = DashboardService(finance_repo, company_repo, sector_repo, sp_500_repo)
        self.sectors = self.dashboard_service.get_distinct_company_data(key="sector")
        self.last_selldate = datetime(year=2025,month=12,day=31)
        self.first_buydate = datetime(year=2008,month=12,day=31)

    def run(self):
        
        res_cols =["buyyear", "sellyear", "sector", "rendite", "strategy"]
        df_result = pd.DataFrame(columns=res_cols)

        for sector in self.sectors:
            buydate = self.first_buydate
            while buydate <= self.last_selldate:
                df_top10 = self.getRanking(buydate, sector)
                if df_top10 is not None:
                    df_top10 = self.getDatePrices(colname="buy_price", date=buydate, df=df_top10)
                    selldate = buydate + relativedelta(years=1)

                    while selldate <= self.last_selldate:
                        df_top10_w_sell = self.getDatePrices("sell_price", selldate, df_top10)

                        df_top10_w_sell["end_value"] = (100 / df_top10_w_sell["buy_price"]) * df_top10_w_sell["sell_price"]
                        portfolio_value_beginning = 1000
                        time_delta = relativedelta(selldate, buydate).years

                        df_grouped = df_top10_w_sell.groupby("strategy", as_index=False)["end_value"].sum()
                        df_grouped["rendite"] = df_grouped["end_value"].apply(lambda s: calc_cagr(s, portfolio_value_beginning, time_delta))


                        df_grouped["sector"] = sector
                        df_grouped["buyyear"] = buydate.year
                        df_grouped["sellyear"] = selldate.year

                        df_result = pd.concat([df_result, df_grouped[res_cols]])

                        selldate += relativedelta(years=1)
                    
                else:
                    df_grouped = pd.DataFrame({"strategy" : ["momentum_score", "value_score"]})
                    df_grouped["sector"] = sector
                    df_grouped["buyyear"] = buydate.year
                    df_grouped["sellyear"] = selldate.year
                    df_grouped["rendite"] = None
                buydate += relativedelta(years=1)

        return df_result

    def getIndexData(self):

        res_cols =["buyyear", "sellyear", "index", "rendite", "strategy"]
        df_result = pd.DataFrame(columns=res_cols)
        indizes = ["SPXEW", "GSPC"]
        
        for index in indizes:
            buydate = self.first_buydate
            while buydate <= self.last_selldate:
                buy_price = self.getIndexPrices(buydate, index)
                selldate = buydate + relativedelta(years=1)
                while selldate <= self.last_selldate:
                    sell_price = self.getIndexPrices(selldate, index)
                    end_value = (100 / buy_price) * sell_price
                    portfolio_value_beginning = 100
                    time_delta = relativedelta(selldate, buydate).years
                    df = pd.DataFrame([{
                        "rendite": calc_cagr(end_value, portfolio_value_beginning, time_delta),
                        "index": index,
                        "buyyear": buydate.year,
                        "sellyear": selldate.year,
                        "strategy": f"passive_{index}"
                    }])

                    df_result = pd.concat([df_result, df], ignore_index=True)
                    selldate += relativedelta(years=1)
                buydate += relativedelta(years=1)
        df_result.head()
        return df_result


    def getRanking(self, date, sector):
        '''
        uses ranking service and returns a df with the top10 in both strategies.
        returns df(symbol, strategy, rank(?), date)
        '''
        ranking_service = RankingService(finance_repo=self.finance_repo, constituents_repo =  self.constituents_repo, \
                                     company_repo=self.company_repo, sector_repo=self.sector_repo, date=date, sector=sector)

        ranking = ranking_service.get_ranking()
        company_data = self.dashboard_service.get_all_company_data(filter={"sector":sector})

        df_rank = pd.DataFrame(ranking)
        df_company = pd.DataFrame(company_data)

        df_enriched = pd.merge(df_rank, df_company,  how="left", on="symbol")
        df_cleaned = df_enriched.reset_index(drop=True)

        df_value = df_cleaned[["symbol", "value_score"]].dropna().\
            sort_values(by="value_score", ascending=False).reset_index(drop=True)[:10]
        df_momentum = df_cleaned[["symbol", "momentum_score"]].dropna().\
            sort_values(by="momentum_score", ascending=False).reset_index(drop=True)[:10]

        df_value = pd.melt(df_value, id_vars=["symbol"], value_vars=["value_score"], var_name="strategy", value_name="score")
        df_momentum = pd.melt(df_momentum, id_vars=["symbol"], value_vars=["momentum_score"], var_name="strategy", value_name="score")

        df_final = pd.concat([df_momentum, df_value]).reset_index(drop=True)

        df_final["date"] = date

        if len(df_value.index) < 10 or len(df_momentum.index) < 10:
            logger.warning(f"Less than 10 Companies in {sector} on {date}")
            return None

        return df_final

    def getDatePrices(self, colname, date, df):
        '''
        enriches dataframe w columns symbol, date, with the adjclosed values of the given date or te latest available value
        return df
        '''
        df[colname] = df["symbol"].apply(lambda s: self.dashboard_service.get_last_available_adj_closed(s, date=date)["adjClose"])
        return df
    
    def getIndexPrices(self, date, symbol):
        '''
        enriches dataframe w columns symbol, date, with the adjclosed values of the given date or te latest available value
        return df
        '''
        return self.dashboard_service.get_last_available_adj_closed_index(symbol, date=date)["adjClose"]


