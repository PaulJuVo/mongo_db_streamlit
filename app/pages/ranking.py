import streamlit as st
from app.shared.logging import init_logging
import logging
from app.shared.mongo import get_data_edge, dashboard_service, get_sector
from datetime import date, datetime
from app.shared.ranking import get_ranking, create_table


init_logging()
logger = logging.getLogger("Streamlit - ranking")
st.set_page_config(layout="wide")

if 'symbol' not in st.session_state:
    st.session_state.symbol = "TSLA"
st.session_state.sector = dashboard_service.map_symbol_to_sector(symbol=st.session_state.symbol)

st.sidebar.caption(f"Data Edge: {get_data_edge().strftime('%Y-%m-%d'):20}")
date_option = st.sidebar.date_input(label="Date", min_value=date(2011,1,1) ,max_value=get_data_edge())
date1 = datetime(date_option.year, date_option.month, date_option.day)
st.session_state.sector = st.sidebar.selectbox(
    "Sector",
    get_sector(),
    index=get_sector().index(st.session_state.sector)
)

df_ranking = get_ranking(st.session_state.sector, date1)

st.markdown("### Stock Ranking")
tab1, tab2 = st.tabs(["Top 10 Value Stocks", "Top 10 Momentum Stocks"])

with tab1:
    create_table(df_ranking,sort_by="value_score", ascending=False, limit=10, caption="Value Score", symbol=None,show_company=False)

with tab2:
    create_table(df_ranking,sort_by="momentum_score", ascending=False, limit=10, caption="Momentum Score", symbol=None,show_company=False)