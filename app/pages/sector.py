import streamlit as st
from app.shared.logging import init_logging
import logging
from app.shared.mongo import get_data_edge, dashboard_service
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
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

if 'symbol' not in st.session_state:
    st.session_state.symbol = "TSLA"
st.session_state.sector = dashboard_service.map_symbol_to_sector(symbol=st.session_state.symbol)

st.session_state.sector = st.sidebar.selectbox(
    "Sector",
    get_sector(),
    index=get_sector().index(st.session_state.sector)
)


symbols = get_symbols(st.session_state.sector)
symbol_options = st.sidebar.multiselect(
    "Companies",
    symbols,
    default=[st.session_state.symbol] if st.session_state.symbol in symbols else []
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
st.title(f"{st.session_state.sector}")
if ratio and st.session_state.sector:
    try:
        st.subheader(f"{ratios[ratio]}")

        with st.container():    
            
            col0, col1, col2, col3 = st.columns([2,3,3,3])
            col0.space("xxsmall")
            col0.space("xxsmall")
            col0.caption(f"Trailing Median")
            tup = dashboard_service.get_sector_median_data_last_years(st.session_state.sector, ratio + "Median", datetime(to_date.year, to_date.month, to_date.day))
            last_year, five_year, ten_year = map(lambda x: round(x,2) if x is not None else None, tup)
            with col1:
                st.metric(label=f"1 Year", value=last_year)
            with col2:
                st.metric(label=f"5 Year", value=five_year)
            with col3:
                st.metric(label=f"10 Year", value=ten_year)


        df_ts = dashboard_service.get_finance_data(companies=symbol_options, 
                                               from_date=datetime(from_date.year, from_date.month, from_date.day), 
                                               to_date=datetime(to_date.year, to_date.month, to_date.day),
                                               )
        
        df_sector = pd.DataFrame(dashboard_service.get_sector_data(sector=st.session_state.sector,
                                                      from_date=datetime(from_date.year, from_date.month, from_date.day), 
                                               to_date=datetime(to_date.year, to_date.month, to_date.day)
                                                    ))


        fig = px.line(
            df_ts,
            x="date",
            y=ratio,
            color="symbol",
            line_shape="spline",
            color_discrete_sequence=px.colors.qualitative.Safe
        )

        fig.update_traces(
            line=dict(width=2),
            opacity=0.8
        )
        # Sektor-Medianlinie hinzufügen
        median_col = ratio + "Median"
        fig.add_trace(
            go.Scatter(
                x=df_sector["date"],
                y=df_sector[median_col],
                mode="lines",
                name=f"Sektor-Median ({st.session_state.sector})",
                line=dict(
                    color="red",
                    width=2,        # dicker als die anderen (die haben width=2)
                    dash="solid"     
                ),
                opacity=1 
            )
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







