from typing import Optional
import streamlit as st
from searchbar_component import searchbar
from core.application.dashboard_service import DashboardService
from core.exceptions.dashboard_exceptions import NoDataFound
from infrastructure.mongo.mongo_repository import MongoRepository
from config.mongo_config import MongoCollection, MongoDatabase, MongoUser
from app.shared.mongo import get_mongo, get_data_edge, dashboard_service
import plotly.express as px
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import re

@st.cache_data
def get_suggestions(query):
    clean_query = re.sub(r'[^a-zA-Z0-9\s]', '', query)
    result =  dashboard_service.get_company_suggestions(filter={"$or": [{"companyName":
                                                                {"$regex": clean_query, 
                                                                 "$options": "i"}},
                                                                 {"symbol":
                                                                {"$regex": clean_query, 
                                                                 "$options": "i"}}
                                                                 ]})
    return [*result]

def search_function(query : str):
    lis = get_suggestions(query)
    return [{"label": f"{v['symbol']:<8} - {v['companyName']}", "value": v["symbol"]} for v in lis]


def get_finance_data():
    df_ts = dashboard_service.get_finance_data(companies=[st.session_state.symbol], 
                                                    from_date=datetime(from_date.year, from_date.month, from_date.day), 
                                                    to_date=datetime(to_date.year, to_date.month, to_date.day), 
                                                    projection=["date", "symbol", "adjClose", ratio])
    return pd.DataFrame(df_ts)

def get_cagr_data(symbol, index):
    data : list[tuple] = []
    years = [1,3,5,10]
    for number in years:
        sp = dashboard_service.get_sp500data_cagr(index, datetime(to_date.year, to_date.month, to_date.day), number)
        fd = dashboard_service.get_financedata_cagr(symbol, datetime(to_date.year, to_date.month, to_date.day), number)
        stri = f"{number}{"Y" if number == 1 else "Y Ann."}"
        data.append((stri, fd, sp))
    return data


def leveled_stockdata(index):
    df_ts = get_finance_data()
    df_sp500 = dashboard_service.get_sp500_data(index=index, from_date=datetime(from_date.year, from_date.month, from_date.day), 
                                                    to_date=datetime(to_date.year, to_date.month, to_date.day))
    df_sp500 = pd.DataFrame(df_sp500)
    df_ts["norm"] = df_ts["adjClose"] / df_ts["adjClose"].iloc[0] * 100
    df_sp500["norm"] = df_sp500["adjClose"] / df_sp500["adjClose"].iloc[0] * 100
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_ts["date"],
            y=df_ts["norm"],
            name=st.session_state.symbol,
            mode="lines"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df_sp500["date"],
            y=df_sp500["norm"],
            name="S&P 500",
            mode="lines",
            line=dict(color="#9aa3aa")
        )
    )
    fig.update_layout(
        template="plotly_dark",
        hovermode="x unified",
        yaxis_title="Performance (Start = 100)"
    )
    st.plotly_chart(fig, width="stretch")
            
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
    st.sidebar.caption(f"Data Edge: {get_data_edge().strftime('%Y-%m-%d'):20}")
    from_date = st.sidebar.date_input(label="From Date", value=def_from_date, min_value=min_date)
    to_date = st.sidebar.date_input(label="To Date", max_value=get_data_edge())
    sector_name = dashboard_service.map_symbol_to_sector(st.session_state.symbol)
    


    #######




    data_company = dashboard_service.get_company_data(filter={"symbol" : st.session_state.symbol})
    if data_company:
        company_name = data_company["companyName"]
        company_symbol = data_company["symbol"]
        company_sector = data_company["sector"]
        company_image = data_company["image"]
        st.space("medium")
        col1, col2, col3 = st.columns(3, vertical_alignment="top")
        with col1:
            con1 = st.container(border=False)
            con1.markdown(
                f"""
                <div style="font-size: 0.9rem; color: gray;">Company Name</div>
                <div style="font-size: 1.8rem; font-weight: 600;">{company_name}</div>
                """,
                unsafe_allow_html=True
            )
        with col2:
            con2 = st.container(border=False)
            con2.markdown(
                f"""
                <div style="font-size: 0.9rem; color: gray;">Symbol</div>
                <div style="font-size: 1.8rem; font-weight: 600;">{company_symbol}</div>
                """,
                unsafe_allow_html=True
            )
        with col3:
            con3 = st.container(border=False)
            con3.markdown(
                f"""
                <div style="font-size: 0.9rem; color: gray;">Sector</div>
                <div style="font-size: 1.8rem; font-weight: 600;">{company_sector}</div>
                """,
                unsafe_allow_html=True
            )
        st.divider()
    
    with st.container(horizontal_alignment="left"):
        ratios = {"peRatio": "Price / Earnings",
              "psRatio": "Price / Sales",
              "pcRatio": "Price / Operating Cashflow",
              "pfcfRatio": "Price / Free Cashflow"}

        ratio = st.pills("Ratios", 
                             options=ratios.keys(), 
                             format_func=lambda option: ratios[option], 
                             selection_mode="single",
                             default="peRatio",
                             label_visibility="hidden")
    if ratio:
        try:
            with st.container():         
                df_ts = get_finance_data()

                fig = make_subplots(specs=[[{"secondary_y": True}]])
                # Ratio (linke Achse)
                # adjClose (rechte Achse)
                
                fig.add_trace(
                    go.Scatter(
                        x=df_ts["date"],
                        y=df_ts["adjClose"],
                        name="Adj Close",
                        mode="lines",
                        line=dict(width=2),
                    ),
                    secondary_y=True
                )
                fig.add_trace(
                    go.Scatter(
                        x=df_ts["date"],
                        y=df_ts[ratio],
                        name=ratios[ratio],
                        mode="lines",
                        line=dict(width=2, dash="dot"),
                    ),
                    secondary_y=False
                )
            
                fig.update_layout(
                    template="plotly_dark",
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
                    title_text=ratios[ratio],
                    zeroline=False,
                    secondary_y=False
                )

                fig.update_yaxes(
                    title_text="Adjusted Close",
                    zeroline=False,
                    secondary_y=True
                )
                st.plotly_chart(fig, width="stretch")
           
            with st.container():    
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    company_median = dashboard_service.get_company_median_data(st.session_state.symbol, 
                                                                               ratio=ratio, 
                                                                               from_date=datetime(from_date.year, from_date.month, from_date.day), 
                                                                               to_date=datetime(to_date.year, to_date.month, to_date.day))
                    st.metric(label=f"{st.session_state.symbol} {ratios[ratio]} Median", value=company_median)
                with col2:
                    company_median = dashboard_service.get_sector_median_data(sector_name, 
                                                                               ratio=ratio + "Median", 
                                                                               from_date=datetime(from_date.year, from_date.month, from_date.day), 
                                                                               to_date=datetime(to_date.year, to_date.month, to_date.day))
                    st.metric(label=f"{sector_name} {ratios[ratio]} Median", value=company_median)
                with col3:
                    company_median = dashboard_service.get_sector_median_data(sector_name, 
                                                                               ratio=ratio + "Median", 
                                                                               from_date=datetime(from_date.year, from_date.month, from_date.day), 
                                                                               to_date=datetime(to_date.year, to_date.month, to_date.day))
                    st.metric(label=f"Z-Score {ratios[ratio]}", value=1.12)
                with col4:
                    company_median = dashboard_service.get_sector_median_data(sector_name, 
                                                                               ratio=ratio + "Median", 
                                                                               from_date=datetime(from_date.year, from_date.month, from_date.day), 
                                                                               to_date=datetime(to_date.year, to_date.month, to_date.day))
                    st.metric(label=f"Overall Score for {st.session_state.symbol}", value=11.27)
        
                            
            with st.container():
                st.divider()
                st.subheader(f"{st.session_state.symbol} vs S&P 500", text_alignment="center")    
                leveled_stockdata("GSPC")
                st.caption(f"Since {to_date}")
            
                symbol = st.session_state.symbol

                data = get_cagr_data(symbol, "GSPC")

                rows = []
                for period, stock, sp in data:
                    delta = stock - sp
                    sign = "+" if delta > 0 else ""
                    rows.append([period, f"{stock:.2f}%", f"{sp:.2f}%", f"{sign}{delta:.2f}%"])

                df = pd.DataFrame(
                    rows,
                    columns=["Period", symbol, "S&P 500", "Delta"],
                )
                # Styler-Funktion für Delta
                def highlight_delta(val):
                    # val ist z.B. "+2.30%" oder "-1.50%"
                    num = float(val.strip("%").replace("+", ""))
                    color = "#09ab3b" if num > 0 else "#ff2b2b" if num < 0 else "white"
                    return f"color: {color}; font-weight: bold"

                st.dataframe(df.style.map(highlight_delta, subset=["Delta"]), width="stretch", hide_index=True) # type: ignore
        except NoDataFound as e:
            st.info(e.message)