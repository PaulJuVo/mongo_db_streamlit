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
from datetime import datetime

init_logging()
logger = logging.getLogger("Streamlit - Dashboard")

st.title("Dashboard")

conn = get_mongo(MongoUser.DASHBOARDUSER)
finance_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.FINANCEDATA)
company_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.COMPANYDATA)
dashboard_service = DashboardService(finance_repo=finance_repo, company_repo=company_repo)

@st.cache_data
def get_industry():
    result =  dashboard_service.get_company_data(key="industry")
    return result

@st.cache_data
def get_symbols(industry):
    result = dashboard_service.get_company_data(key="symbol", filter = {"industry" : industry})
    
    return result

industry_option = st.selectbox(
    "Chose the Industry",
    get_industry(),
)


symbols = get_symbols(industry_option)

options1 = st.multiselect(
    "What are your favorite colors?",
    symbols,
    default=symbols[0],
)

current_time = date.today()
def_from_date = current_time - relativedelta(years=2)

from_date = st.date_input(label="From Date", value=def_from_date)
to_date = st.date_input(label="To Date")

try: 
    df_ts = dashboard_service.get_finance_data(companies=options1, 
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







