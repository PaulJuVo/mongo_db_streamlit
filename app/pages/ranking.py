import streamlit as st
from app.shared.logging import init_logging
import logging
from infrastructure.mongo.mongo_repository import MongoRepository
from config.mongo_config import MongoCollection, MongoDatabase, MongoUser
from app.shared.mongo import get_mongo, get_data_edge, dashboard_service
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import plotly.express as px
from core.application.ranking_service import RankingService
from core.exceptions.dashboard_exceptions import NoDataFound
from app.shared.mongo import get_sector
import pandas as pd

init_logging()
logger = logging.getLogger("Streamlit - ranking")
st.set_page_config(layout="wide")
st.sidebar.caption(f"Data Edge: {get_data_edge().strftime('%Y-%m-%d'):20}")

date_option = st.sidebar.date_input(label="Date", min_value=date(2010,1,1) ,max_value=get_data_edge())
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
tab1, tab2 = st.tabs(["Top 5 Value Stocks", "Top 5 Momentum Stocks"])
df_rank = pd.DataFrame(ranking)
df_company = pd.DataFrame(company_data)
df_enriched = pd.merge(df_rank, df_company,  how="left", on="symbol")
to_drop = ["psRatio", "peRatio", "pcRatio", "pfcfRatio"]
to_drop = to_drop + [v + "_z_score" for v in to_drop] + ["_id", "sector"]
df_cleaned = df_enriched.drop(columns=to_drop).dropna()
cols = ["image"] + [c for c in df_cleaned.columns if c != "image"]
df_cleaned = df_cleaned[cols]



with tab1:
    st.space("xxsmall")
    df_sorted = df_cleaned.sort_values(by="value_score", ascending=False)
    df_top5 = df_sorted.head(5)
    cols = st.columns([1, 1, 4, 1])
    #cols[0].caption("", width=40)
    #cols[1].caption("Symbol")
    #cols[2].caption("Company Name")
    cols[3].caption("Value Score")
    for _, row in df_top5.iterrows():
        cols = st.columns([1, 1, 4, 1])
        cols[0].image(row["image"], width=40)
        cols[1].markdown(f"**{row['symbol']}**")
        cols[2].markdown(f"{row['companyName']}")
        cols[3].markdown(f"{row['value_score']:.2f}")

with tab2:
    df_sorted = df_cleaned.sort_values(by="value_score", ascending=True)
    df_top5 = df_sorted.head(5)
    st.markdown("### Stock Ranking")
    for _, row in df_top5.iterrows():
        cols = st.columns([1, 1, 4, 1])
        cols[0].image(row["image"], width=40)
        cols[1].markdown(f"**{row['symbol']}**")
        cols[2].markdown(f"{row['companyName']}")
        cols[3].markdown(f"{row['value_score']:.2f}")

# st.dataframe(ranking)