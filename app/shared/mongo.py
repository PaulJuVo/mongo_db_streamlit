from infrastructure.mongo.mongo_connection import MongoConnection
from infrastructure.mongo.mongo_repository import MongoRepository
from config.mongo_config import MongoUser, MongoCollection, MongoDatabase
from core.application.dashboard_service import DashboardService
import streamlit as st

@st.cache_resource
def get_mongo(user : MongoUser):
    conn = MongoConnection(user)
    conn.connect()
    return conn

def _get_dashboard_service():
    conn = get_mongo(MongoUser.DASHBOARDUSER)
    finance_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.FINANCEDATA)
    company_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.COMPANYDATA)
    sector_repo = MongoRepository(conn,  MongoDatabase.PROCESSED, MongoCollection.SECTORDATA)
    sp_500_repo = MongoRepository(conn,  MongoDatabase.PROCESSED, MongoCollection.SP500)
    return DashboardService(finance_repo=finance_repo, company_repo=company_repo, sector_repo=sector_repo, sp_500_repo=sp_500_repo)

dashboard_service = _get_dashboard_service()

@st.cache_data
def get_sector():
    result =  dashboard_service.get_distinct_company_data(key="sector")
    return result

@st.cache_data
def get_symbols(sector):
    result = dashboard_service.get_distinct_company_data(key="symbol", filter = {"sector" : sector})
    return result

@st.cache_data
def get_data_edge():
    dataedge = dashboard_service.get_data_edge()
    return dataedge

