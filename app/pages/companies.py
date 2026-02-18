import streamlit as st
from searchbar_component import searchbar
from core.application.dashboard_service import DashboardService
from infrastructure.mongo.mongo_repository import MongoRepository
from config.mongo_config import MongoCollection, MongoDatabase, MongoUser
from app.shared.mongo import get_mongo
import plotly.express as px
import pandas as pd
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

conn = get_mongo(MongoUser.DASHBOARDUSER)
finance_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.FINANCEDATA)
company_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.COMPANYDATA)
dashboard_service = DashboardService(finance_repo=finance_repo, company_repo=company_repo)

@st.cache_data
def get_suggestions(query):
    rege = f"^{query}"
    result =  dashboard_service.get_company_suggestions(filter={"companyName":
                                                                {"$regex": rege, "$options": "i"}})
    return [*result]

def search_function(query):
    lis = get_suggestions(query)
    return [{"label": v["companyName"], "value": v["symbol"]} for v in lis]

st.title("Search Company Data")

if 'symbol' not in st.session_state:
    st.session_state.symbol = "APPL"
if 'query' not in st.session_state:
    st.session_state['query'] = 'a'

# Call the function to get suggestions
suggestions = search_function(st.session_state.query)

result = searchbar(
    key="my_searchbar",
    placeholder="select a company...",
    suggestions=suggestions,  # This should be the return value of the function
    highlightBehavior="keep",  # Options: "keep", "update", "partial" 
    show_plus_button=False,
    style_overrides={
        "clear": {"fill": "#ff0000"},
        "plus": {"fill": "#00ff00"},
    }
)

if result:
    if result.get("interaction") == "search":
        st.session_state.query = result["value"]
        # Update suggestions based on the search query

    elif result.get("interaction") == "select":
        selected = result["value"]
        st.session_state.symbol = selected["value"]

    elif result.get("interaction") == "submit":
        st.warning("Select a Company", icon="🫨")

    elif result.get("interaction") == "reset":
        st.session_state.query = ""
    
    current_time = date.today()
    def_from_date = current_time - relativedelta(years=2)
    min_date = date(2010,1,1)
    from_date = st.sidebar.date_input(label="From Date", value=def_from_date, min_value=min_date)
    to_date = st.sidebar.date_input(label="To Date")
    
    data_company = dashboard_service.get_company_data(filter={"symbol" : st.session_state.symbol})
    company_name = data_company["companyName"]
    company_symbol = data_company["symbol"]
    company_industry = data_company["industry"]
    col1, col2, col3 = st.columns(3, vertical_alignment="top")
    with col1:
        con1 = st.container(border=False)
        con1.write("Company Name")
        con1.subheader(company_name)
    with col2:
        con2 = st.container(border=False)
        con2.write("Symbol")
        con2.subheader(company_symbol)
    with col3:
        con3 = st.container(border=False)
        con3.write("Industry")
        con3.subheader(company_industry)
    try:
        df_ts = dashboard_service.get_finance_data(companies=[st.session_state.symbol], 
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
        st.info("No Data found: Check filter conditions")