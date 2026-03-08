import streamlit as st
from app.shared.logging import init_logging
import logging
from infrastructure.mongo.mongo_repository import MongoRepository
from config.mongo_config import MongoCollection, MongoDatabase, MongoUser
from app.shared.mongo import get_mongo, get_data_edge, dashboard_service
from datetime import date, datetime
import plotly.express as px
from core.application.ranking_service import RankingService
from core.exceptions.dashboard_exceptions import NoDataFound
from app.shared.mongo import get_sector
import pandas as pd


init_logging()
logger = logging.getLogger("Streamlit - ranking")
st.set_page_config(layout="wide")
st.sidebar.caption(f"Data Edge: {get_data_edge().strftime('%Y-%m-%d'):20}")

date_option = st.sidebar.date_input(label="Date", min_value=date(2011,1,1) ,max_value=get_data_edge())
date1 = datetime(date_option.year, date_option.month, date_option.day)
sector_option = st.sidebar.selectbox(
    "Sector",
    get_sector(),
)
conn = get_mongo(MongoUser.DASHBOARDUSER)
finance_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.FINANCEDATA)
company_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.COMPANYDATA)
sector_repo = MongoRepository(conn,  MongoDatabase.PROCESSED, MongoCollection.SECTORDATA)
ranking_service = RankingService(finance_repo=finance_repo, company_repo=company_repo, sector_repo=sector_repo, date=date1, sector=sector_option)

ranking = ranking_service.get_ranking()

company_data = dashboard_service.get_all_company_data(filter={"sector":sector_option})
st.markdown("### Stock Ranking")
tab1, tab2 = st.tabs(["Top 10 Value Stocks", "Top 10 Momentum Stocks"])
df_rank = pd.DataFrame(ranking)
df_company = pd.DataFrame(company_data)
df_enriched = pd.merge(df_rank, df_company,  how="left", on="symbol")
to_drop = ["psRatio", "peRatio", "pcRatio", "pfcfRatio"]
to_drop = to_drop + [v + "_z_score" for v in to_drop] + ["_id", "sector"]
df_cleaned = df_enriched.drop(columns=to_drop).dropna()
cols = ["image"] + [c for c in df_cleaned.columns if c != "image"]
df_cleaned = df_cleaned[cols]



def create_table(df_cleaned : pd.DataFrame, sort_by : str, ascending : bool, limit : int, caption : str):
    df_sorted = df_cleaned.sort_values(by=sort_by, ascending=ascending)
    df_top5 = df_sorted.head(limit)
    # Header
    st.markdown("<div style='margin-top:2px;'></div>", unsafe_allow_html=True)
    cols = st.columns([1, 1, 4, 1])
    cols[3].caption(caption)

    for _, row in df_top5.iterrows():
        cols = st.columns([1, 1, 4, 1])
        cols[0].markdown(
            f"""
            <div style="
                width:40px;
                height:40px;
                display:flex;
                align-items:center;
                justify-content:center;
                padding:2px;
            ">
                <img src="{row['image']}" style="max-width:40px; max-height:40px; border-radius:6px;">
            </div>
            """,
            unsafe_allow_html=True
        )
        cols[1].markdown(
            f"""
            <div style="display:flex; flex-direction:column; justify-content:center; height:40px;">
                <strong>{row['symbol']}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )
        cols[2].markdown(
            f"""
            <div style="display:flex; flex-direction:column; justify-content:center; height:40px;">
                {row['companyName']}
            </div>
            """,
            unsafe_allow_html=True
        )
        cols[3].markdown(
            f"""
            <div style="display:flex; align-items:center; justify-content:flex-start; height:40px;">
                {row[sort_by]:.2f}
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<div style='margin-top:4px;'></div>", unsafe_allow_html=True)


with tab1:
    create_table(df_cleaned, "value_score", True, 10, "Value Score")

with tab2:
    create_table(df_cleaned, "value_score", False, 10, "Value Score")
        

        

# st.dataframe(ranking)