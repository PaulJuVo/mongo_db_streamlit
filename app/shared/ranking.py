from typing import Optional
import streamlit as st
from infrastructure.mongo.mongo_repository import MongoRepository
from config.mongo_config import MongoCollection, MongoDatabase, MongoUser
from app.shared.mongo import get_mongo, dashboard_service
from core.application.ranking_service import RankingService
import pandas as pd



@st.cache_data
def get_ranking(sector, date1) -> pd.DataFrame:

    conn = get_mongo(MongoUser.DASHBOARDUSER)
    finance_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.FINANCEDATA)
    company_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.COMPANYDATA)
    sector_repo = MongoRepository(conn,  MongoDatabase.PROCESSED, MongoCollection.SECTORDATA)

    ranking_service = RankingService(finance_repo=finance_repo, company_repo=company_repo, sector_repo=sector_repo, date=date1, sector=sector)
    ranking = ranking_service.get_ranking()
    company_data = dashboard_service.get_all_company_data(filter={"sector":sector})
    df_rank = pd.DataFrame(ranking)
    df_company = pd.DataFrame(company_data)
    df_enriched = pd.merge(df_rank, df_company,  how="left", on="symbol")
    df_cleaned = df_enriched.dropna(subset=["value_score"]).reset_index(drop=True)
    cols = ["image"] + [c for c in df_cleaned.columns if c != "image"]
    df_cleaned = df_cleaned[cols]
    return df_cleaned

@st.cache_data
def sort_ranking(df_cleaned, sort_by, ascending):
    df_sorted = df_cleaned.sort_values(by=sort_by, ascending=ascending).reset_index(drop=True)
    # Ranking erzeugen
    df_sorted["rank"] = df_sorted.index + 1
    return df_sorted

def get_company_ranked(df_sorted, symbol):
    df_symbol = df_sorted[df_sorted["symbol"] == symbol]
    return df_symbol

def print_ranking_row(row, score):
        cols = st.columns([1, 1, 1, 4, 1])
        # Rank
        cols[0].markdown(
            f"""
            <div style="display:flex; align-items:center; justify-content:flex-start; height:40px;">
                {int(row['rank'])}
            </div>
            """,
            unsafe_allow_html=True
        )
        cols[1].markdown(
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
        cols[2].markdown(
            f"""
            <div style="display:flex; flex-direction:column; justify-content:center; height:40px;">
                <strong>{row['symbol']}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )
        cols[3].markdown(
            f"""
            <div style="display:flex; flex-direction:column; justify-content:center; height:40px;">
                {row['companyName']}
            </div>
            """,
            unsafe_allow_html=True
        )
        cols[4].markdown(
            f"""
            <div style="display:flex; align-items:center; justify-content:center; height:40px;">
                {row[score]:.2f}
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<div style='margin-top:4px;'></div>", unsafe_allow_html=True)

def create_table(df_ranking,sort_by: str, ascending: bool, limit: int = 1000, symbol : Optional[str] = None, caption: str = "Value Score", show_company : bool = False):

    df_sorted = sort_ranking(df_ranking, sort_by=sort_by, ascending=ascending)
    df_top = df_sorted.head(limit)
    
    # Header
    
    st.markdown("<div style='margin-top:2px;'></div>", unsafe_allow_html=True)
    cols = st.columns([1, 2, 2, 4, 1])

    if show_company and symbol:
        df_symbol = get_company_ranked(df_sorted, symbol)
        with st.container(border=True, ):
            print_ranking_row(df_symbol.iloc[0], sort_by)
        st.markdown("<div style='margin-top:2px;'></div>", unsafe_allow_html=True)

    cols[0].caption("Ranking No.")
    cols[4].caption(caption)
    for _, row in df_top.iterrows():
        print_ranking_row(row, sort_by)