
from core.interfaces.base_repository_interface import BaseRepositoryInterface
from datetime import datetime
from config.logging_config import performance_log
from config.mongo_config import FINANCEDATA_TIMESERIES_CONFIG
from config.pipeline_config import COMPANY_PIPELINE, INCOME_STAGED, EOD_STAGED, CASHFLOW_STAGED, CONSTITUES, SECTOR_DATA, SP500
from core.domain.validation import contains_right_income_statements, contains_right_cashflow_statements
from core.domain.calculation import calc_ratio, calc_per_share_ttm, get_avg_shares, calc_ttm_eps
import logging
import pandas as pd

logger = logging.getLogger(__name__)

class PipelineService:
    def __init__(self, 
                 eodprice_repo : BaseRepositoryInterface, 
                 income_repo : BaseRepositoryInterface,
                 cashflow_repo : BaseRepositoryInterface,
                 staged_eodprice_repo : BaseRepositoryInterface, 
                 staged_income_repo : BaseRepositoryInterface,
                 staged_cashflow_repo : BaseRepositoryInterface,
                 profile_repo : BaseRepositoryInterface,
                 financedata_repo : BaseRepositoryInterface,
                 company_repo : BaseRepositoryInterface,
                 constituents_repo : BaseRepositoryInterface,
                 scd_constituents_repo : BaseRepositoryInterface,
                 sector_repo : BaseRepositoryInterface,
                 sp500_raw_repo : BaseRepositoryInterface,
                 sp500_repo : BaseRepositoryInterface
                 ):
        self.eodprice_repo = eodprice_repo
        self.income_repo = income_repo
        self.staged_eodprice_repo = staged_eodprice_repo
        self.staged_income_repo = staged_income_repo
        self.profile_repo = profile_repo
        self.financedata_repo = financedata_repo
        self.company_repo = company_repo
        self.staged_cashflow_repo = staged_cashflow_repo
        self.cashflow_repo = cashflow_repo
        self.constituents_repo = constituents_repo
        self.scd_constituents_repo = scd_constituents_repo
        self.sector_repo = sector_repo
        self.sp500_raw_repo = sp500_raw_repo
        self.sp500_repo=sp500_repo


    def run(self):
        self.create_scd_constituents()
        # self.upsert_company_data()
        # self.create_sp500_timeseries()
        # self.upsert_eod_staged()
        # self.upsert_income_staged()
        # self.upsert_cashflow_staged()
        # self.create_finance_data(2000)
        # self.create_sector_timeseries()
        
    
    @performance_log(logger)
    def create_finance_data(self, b_size):
        self.financedata_repo.drop()
        self.financedata_repo.create_time_series(config=FINANCEDATA_TIMESERIES_CONFIG)

        results = self.staged_eodprice_repo.find(batch_size=b_size)
        to_copy = ["date", "adjClose", "symbol"]
        processed_data = []
        batch_size = 1000

        income_docs = self.staged_income_repo.find(sort={"symbol": 1, "fillingDate": 1})
        cashflow_docs = self.staged_cashflow_repo.find(sort={"symbol": 1, "fillingDate": 1})

        income_grouped = {}
        for doc in income_docs:
            income_grouped.setdefault(doc["symbol"], []).append(doc)

        cashflow_grouped = {}
        for doc in cashflow_docs:
            cashflow_grouped.setdefault(doc["symbol"], []).append(doc)


        for eod_price in results:
            finance_data = {k: v for k, v in eod_price.items() if k in to_copy}
            date = eod_price["date"]
            symbol = eod_price["symbol"]

            income_list = income_grouped.get(symbol, [])
            incom_stats = [i for i in income_list if i["fillingDate"] <= date][-4:]
            cashflow_list = cashflow_grouped.get(symbol, [])
            cashflow_stats = [i for i in cashflow_list if i["fillingDate"] <= date][-4:]

            if contains_right_income_statements(incom_stats, eod_price["date"]):
                avg_shares_ttm = get_avg_shares(incom_stats)
                eps_ttm = calc_ttm_eps(incom_stats)
                rev_p_share_ttm = calc_per_share_ttm(incom_stats, avg_shares_ttm, "revenue")

                adjclosed = eod_price["adjClose"]

                finance_data["peRatio"] = calc_ratio(eps_ttm, adjclosed)
                finance_data["psRatio"] = calc_ratio(rev_p_share_ttm, adjclosed)

                if contains_right_cashflow_statements(cashflow_stats, eod_price["date"]):
                    free_cashflow_ttm = calc_per_share_ttm(cashflow_stats,avg_shares_ttm, "freeCashFlow")
                    op_cashflow_ttm = calc_per_share_ttm(cashflow_stats,avg_shares_ttm, "operatingCashFlow")

                    finance_data["pfcfRatio"] = calc_ratio(free_cashflow_ttm, adjclosed)
                    finance_data["pcRatio"] = calc_ratio(op_cashflow_ttm, adjclosed)
                
                else:
                    finance_data["pfcfRatio"] = None
                    finance_data["pcRatio"] = None

            else:    
                finance_data["peRatio"] = None
                finance_data["psRatio"] = None
                finance_data["pfcfRatio"] = None
                finance_data["pcRatio"] = None

            processed_data.append(finance_data)
            if len(processed_data) >= batch_size:
                self.financedata_repo.insert_many(processed_data)
                processed_data.clear()
        if processed_data:
            self.financedata_repo.insert_many(processed_data)

    def create_scd_constituents(self):
        self.constituents_repo.execute_pipeline(CONSTITUES)
        self.constituents_repo.create_index(keys=[("removedTicker", 1), ("date", 1)], unique=False)

        events = list(self.constituents_repo.find(sort={"date": 1}))

        active = {}
        scd = []

        earliest_date = events[0]["date"]

        # Schritt 1: Nur echte 1957er add-only Einträge als Gründer
        for e in events:
            added = (e.get("addedSecurity") or "").strip()
            removed = (e.get("removedSecurity") or "").strip()
            ticker = (e.get("symbol") or "").strip()
            if added and not removed and ticker:
                active[ticker] = {
                    "date": e["date"],
                    "symbol": ticker,
                    "companyName": added
                }

        print("Active nach add-only Gründer:", len(active))

        # Schritt 2: Hauptschleife chronologisch – nur Swaps
        for event in events:
            date = event["date"]
            removed_ticker = (event.get("removedTicker") or "").strip()
            removed_name = (event.get("removedSecurity") or "").strip()
            added_name = (event.get("addedSecurity") or "").strip()
            added_ticker = (event.get("symbol") or "").strip()

            if removed_name and added_name:
                if removed_ticker:
                    if removed_ticker in active:
                        scd.append({
                            "companyName": active[removed_ticker]["companyName"],
                            "symbol": removed_ticker,
                            "fromDate": active[removed_ticker]["date"],
                            "toDate": date
                        })
                        del active[removed_ticker]
                    else:
                        # Nicht in active → als Gründer nachträglich eintragen und sofort schließen
                        scd.append({
                            "companyName": removed_name,
                            "symbol": removed_ticker,
                            "fromDate": earliest_date,
                            "toDate": date
                        })

                if added_ticker:
                    active[added_ticker] = {
                        "date": date,
                        "symbol": added_ticker,
                        "companyName": added_name
                    }

        print("Active am Ende:", len(active))

        # Nach der Hauptschleife, vor dem letzten Loop
        from collections import Counter

        # Wie viele unique Ticker sind mehrfach in active?
        ticker_counts = Counter(doc["symbol"] for doc in active.values())
        duplicates = {t: c for t, c in ticker_counts.items() if c > 1}
        print("Duplikate in active:", duplicates)

        # Wie viele SCD-Einträge gibt es pro Ticker mit toDate=2999?
        open_entries = [s for s in scd if s["toDate"] == datetime(2999, 12, 12)]
        print("Offene SCD-Einträge:", len(open_entries))

        # Wie viele Ticker kommen mehrfach offen vor?
        open_tickers = Counter(s["symbol"] for s in open_entries)
        open_duplicates = {t: c for t, c in open_tickers.items() if c > 1}
        print("Offen doppelte Ticker:", open_duplicates)

        # Schritt 3: Alle noch aktiven → offen bis 2999
        for ticker, doc in active.items():
            scd.append({
                "companyName": doc["companyName"],
                "symbol": doc["symbol"],
                "fromDate": doc["date"],
                "toDate": datetime(2999, 12, 12)
            })

        self.scd_constituents_repo.drop()
        self.scd_constituents_repo.insert_many(scd)
        

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

    def upsert_cashflow_staged(self):
        self.staged_cashflow_repo.create_index(keys=[("symbol", 1), ("date", -1)], unique=True)
        self.cashflow_repo.execute_pipeline(CASHFLOW_STAGED)
        self.staged_cashflow_repo.create_index(keys=[("symbol", 1), ("fillingDate", -1)], unique=False)

    def create_sector_timeseries(self):
        self.sector_repo.drop()

        finance_df = pd.DataFrame(list(self.financedata_repo.find(
            projection={"symbol": 1, "date": 1, "pcRatio": 1, 
                       "peRatio": 1, "pfcfRatio": 1, "psRatio": 1, "_id": 0}
        )))

        company_df = pd.DataFrame(list(self.company_repo.find(
            projection={"symbol": 1, "sector": 1, "_id": 0}
        )))

        scd_df = pd.DataFrame(list(self.scd_constituents_repo.find(
            projection={"symbol": 1, "fromDate": 1, "toDate": 1, "_id": 0}
        )))

        df = finance_df.merge(company_df, on="symbol", how="inner")
        df = df[df["sector"].notna()]

        # 3. SCD-Join in Python – merge + Datumsfilter
        df = df.merge(scd_df, on="symbol", how="inner")
        mask = (df["fromDate"] <= df["date"]) & (df["toDate"] >= df["date"])
        df = df[mask].drop(columns=["fromDate", "toDate"])

        rows = []
        for (date, sector), group in df.groupby(["date", "sector"]):
            rows.append({
                "date":            date,
                "sector":          sector,
                "pcRatioMedian":   group["pcRatio"].dropna().median() or None,
                "peRatioMedian":   group["peRatio"].dropna().median() or None,
                "pfcfRatioMedian": group["pfcfRatio"].dropna().median() or None,
                "psRatioMedian":   group["psRatio"].dropna().median() or None
            })

        self.sector_repo.insert_many(rows)
        self.sector_repo.create_index(keys=[("sector", 1), ("date", -1)], unique=False)

    def create_sp500_timeseries(self):
        self.sp500_repo.drop()
        self.sp500_raw_repo.execute_pipeline(SP500)
        self.sp500_repo.create_index(keys=[("date", -1)], unique=False)