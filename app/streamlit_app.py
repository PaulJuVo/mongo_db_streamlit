import streamlit as st
from app.shared.logging import init_logging
import logging
from infrastructure.mongo.mongo_repository import MongoRepository
from config.mongo_config import MongoCollection, MongoDatabase, MongoUser
from app.shared.mongo import get_mongo
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import plotly.express as px
import pandas as pd
from core.application.dashboard_service import DashboardService

from searchbar_component import searchbar
init_logging()
logger = logging.getLogger("Streamlit - Dashboard")

conn = get_mongo(MongoUser.DASHBOARDUSER)
finance_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.FINANCEDATA)
company_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.COMPANYDATA)
dashboard_service = DashboardService(finance_repo=finance_repo, company_repo=company_repo)

@st.cache_data
def get_industry():
    result =  dashboard_service.get_distinct_company_data(key="industry")
    return result

@st.cache_data
def get_symbols(industry):
    result = dashboard_service.get_distinct_company_data(key="symbol", filter = {"industry" : industry})
    
    return result

st.title("Dashboard")

current_time = date.today()
def_from_date = current_time - relativedelta(years=2)
min_date = date(2010,1,1)
from_date = st.sidebar.date_input(label="From Date", value=def_from_date, min_value=min_date)
to_date = st.sidebar.date_input(label="To Date")
industry_option = st.sidebar.selectbox(
    "Industry",
    get_industry(),
)

symbols = get_symbols(industry_option)
symbol_options = st.sidebar.multiselect(
    "Companies",
    symbols,
    default=symbols[0],
)
        
try: 
    df_ts = dashboard_service.get_finance_data(companies=symbol_options, 
                                           from_date=datetime(from_date.year, from_date.month, from_date.day), 
                                           to_date=datetime(to_date.year, to_date.month, to_date.day),
                                           projection=["date", "symbol", "peRatio"])


    fig = px.line(
        df_ts,
        x="date",
        y="peRatio",
        color="symbol",   # separate lines per company
        symbol="symbol",  # different markers per company
        markers=True
    )
    # In Streamlit anzeigen
    st.plotly_chart(fig)
except ValueError:
    st.info("No Data found")







