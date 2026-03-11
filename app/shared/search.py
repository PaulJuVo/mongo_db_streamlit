import streamlit as st
from searchbar_component import searchbar
from app.shared.mongo import dashboard_service
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

