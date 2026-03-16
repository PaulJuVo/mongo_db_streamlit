from enum import Enum
import os

class MongoUser(Enum):
    APPUSER = "appUser"
    DASHBOARDUSER = "dashboardUser"

class MongoDatabase(Enum):
    RAW = "raw"
    PROCESSED = "processed"

class MongoCollection(Enum):
    EODPRICE = "eodPrice"
    INCOMESTATEMENT = "incomeStatement"
    CASHFLOW = "cashflowStatement"
    STAGED_EODPRICE = "stagedEodPrice"
    STAGED_INCOMESTATEMENT = "stagedIncomeStatement"
    STAGED_CASHFLOW = "stagedCashflowStatement"
    PROFILE = "profile"
    FINANCEDATA = "financeData"
    COMPANYDATA = "companyData"
    CONSTITUENTS = "constituents"
    SCD_CONSTITUENTS = "scdConstituents"
    SECTORDATA = "sectorData"
    SP500 = "sp500Data"
    SPXEW = "spxewData"
    

FILTER_QUERIES_UPLOAD = {MongoCollection.PROFILE.value: ["symbol"], 
              MongoCollection.INCOMESTATEMENT.value : ["symbol", "date"],
              MongoCollection.CASHFLOW.value : ["symbol", "date"],
              MongoCollection.EODPRICE.value : ["symbol"]}


FINANCEDATA_TIMESERIES_CONFIG = {
               "timeField": "date",
               "metaField": "symbol",
               "granularity": "hours"
           }

# TODO delete wenn streamlit über docker läuft und prod sein soll 
#from dotenv import load_dotenv
#load_dotenv(".env.dev")

HOST = os.environ["MONGO_HOST"]
PORT = os.environ["MONGO_PORT"]

APPUSER_USER = os.environ["MONGO_APPUSER_USER"]
APPUSER_PASSWORD = os.environ["MONGO_APPUSER_PASSWORD"]
APPUSER_AUTHDB = os.environ["MONGO_APPUSER_AUTH_DB"]

DASHBOARDUSER_USER = os.environ["MONGO_DASHBOARDUSER_USER"]
DASHBOARDUSER_PASSWORD = os.environ["MONGO_DASHBOARDUSER_PASSWORD"]
DASHBOARDUSER_AUTHDB = os.environ["MONGO_DASHBOARDUSER_AUTH_DB"]

APPUSER_URI = f"mongodb://{APPUSER_USER}:{APPUSER_PASSWORD}@{HOST}:{PORT}/{APPUSER_AUTHDB}?authSource={APPUSER_AUTHDB}"
DASHBOARDUSER_URI = f"mongodb://{DASHBOARDUSER_USER}:{DASHBOARDUSER_PASSWORD}@{HOST}:{PORT}/{DASHBOARDUSER_AUTHDB}?authSource={DASHBOARDUSER_AUTHDB}"

