import streamlit as st
from app.shared.logging import init_logging
import logging
from app.shared.mongo import get_data_edge, dashboard_service, get_sector
from datetime import datetime, date
from app.shared.ranking import get_ranking, create_table
from app.shared.search import search_function, searchbar

init_logging()
logger = logging.getLogger("Streamlit - ranking")
st.set_page_config(layout="wide")



if 'symbol' not in st.session_state:
    st.session_state.symbol = "TSLA"
if 'sector' not in st.session_state:
    st.session_state.sector = "Consumer Cyclical"
st.session_state.sector2 = dashboard_service.map_symbol_to_sector(st.session_state.symbol)
if 'query' not in st.session_state:
    st.session_state['query'] = 'a'
if 'strategy' not in st.session_state:
    st.session_state['strategy'] = 'value_score'

st.sidebar.caption(f"Data Edge: {get_data_edge().strftime('%Y-%m-%d'):20}")

date_option = st.sidebar.date_input(label="Date", min_value=date(2011,1,1) ,max_value=get_data_edge())
date1 = datetime(date_option.year, date_option.month, date_option.day)

strategys: dict[str, str] = {"value_score": "Value",
          "momentum_score": "Momentum"}

strategy =st.sidebar.pills("Strategies", 
                         options=strategys.keys(), 
                         format_func=lambda option: strategys[option], 
                         selection_mode="single",
                         default=st.session_state['strategy'])


st.title("Search Ranking Data")

if strategy:
    tab1, tab2 = st.tabs(["by Company Name", "by Sector"])
    with tab2:
        st.session_state.sector = st.selectbox(
            "Sector",
            get_sector(),
            index=get_sector().index(st.session_state.sector)
            )
        st.markdown(f"### {strategys[strategy]} Ranking for {st.session_state.sector} Sector")
        df_ranking = get_ranking(st.session_state.sector, date1)
        create_table(df_ranking,sort_by=strategy, ascending=False, limit=1000, caption=f"{strategys[strategy]} Score", symbol=None,show_company=False)

    with tab1:
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
            st.session_state.sector2 = dashboard_service.map_symbol_to_sector(st.session_state.symbol)

        st.markdown(f"### {strategys[strategy]} Ranking for {st.session_state.sector2} Sector")
        df_ranking = get_ranking(st.session_state.sector2, date1)
        create_table(df_ranking,sort_by=strategy, ascending=False, limit=1000, caption=f"{strategys[strategy]} Score", symbol=st.session_state.symbol,show_company=True)
