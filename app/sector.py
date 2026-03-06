import streamlit as st
from app.shared.logging import init_logging
import logging
from infrastructure.mongo.mongo_repository import MongoRepository
from config.mongo_config import MongoCollection, MongoDatabase, MongoUser
from app.shared.mongo import get_mongo, get_data_edge, dashboard_service
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import plotly.express as px
from core.application.dashboard_service import DashboardService
from core.exceptions.dashboard_exceptions import NoDataFound

init_logging()
logger = logging.getLogger("Streamlit - Dashboard")
st.set_page_config(layout="wide")

@st.cache_data
def get_sector():
    result =  dashboard_service.get_distinct_company_data(key="sector")
    return result

@st.cache_data
def get_symbols(sector):
    result = dashboard_service.get_distinct_company_data(key="symbol", filter = {"sector" : sector})
    
    return result



current_time = date.today()
def_from_date = current_time - relativedelta(years=2)
min_date = date(2010,1,1)
st.sidebar.caption(f"Data Edge: {get_data_edge().strftime('%Y-%m-%d'):20}")
from_date = st.sidebar.date_input(label="From Date", value=def_from_date, min_value=min_date)
to_date = st.sidebar.date_input(label="To Date", max_value=get_data_edge())

sector_option = st.sidebar.selectbox(
    "Sector",
    get_sector(),
)

symbols = get_symbols(sector_option)
symbol_options = st.sidebar.multiselect(
    "Companies",
    symbols,
    default=symbols[0],
)

ratios = {"peRatio": "Price / Earnings",
          "psRatio": "Price / Sales",
          "pcRatio": "Price / Operating Cashflow",
          "pfcfRatio": "Price / Free Cashflow"}

ratio = st.sidebar.pills("Ratios", 
                         options=ratios.keys(), 
                         format_func=lambda option: ratios[option], 
                         selection_mode="single",
                         default="peRatio")
st.title(f"{sector_option}")
if ratio:
    try:
        st.subheader(f"{ratios[ratio]} (Median for Sector)")
        last_year, five_year, ten_year = dashboard_service.get_sector_median_data_last_years(sector_option, ratio + "Median", datetime(to_date.year, to_date.month, to_date.day))
        col1, col2, col3 = st.columns(3, vertical_alignment="top")
        with col1:
            con1 = st.container(border=True)
            con1.write("Last Year")
            con1.subheader(last_year)
        with col2:
            con2 = st.container(border=True)
            con2.write("Last 5 Years")
            con2.subheader(five_year)
        with col3:
            con3 = st.container(border=True)
            con3.write("Last 10 Years")
            con3.subheader(ten_year)

        df_ts = dashboard_service.get_finance_data(companies=symbol_options, 
                                               from_date=datetime(from_date.year, from_date.month, from_date.day), 
                                               to_date=datetime(to_date.year, to_date.month, to_date.day),
                                               projection=["date", "symbol", ratio])


        fig = px.line(
            df_ts,
            x="date",
            y=ratio,
            color="symbol",
            line_shape="spline"
        )

        fig.update_traces(
            line=dict(width=2),
            opacity=0.9
        )
        fig.update_layout(
            template="plotly_white",
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        fig.update_xaxes(
            showgrid=True,
            gridcolor="rgba(200,200,200,0.2)",
            rangeslider_visible=True
        )
        fig.update_yaxes(
            title=ratios[ratio],
            zeroline=False
        )
        st.plotly_chart(fig, width="stretch")
    except NoDataFound as e:
        st.info(e.message, icon="🫨")







