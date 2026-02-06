import streamlit as st
from config.logging_config import setup_logging as _setup_logging

@st.cache_resource
def init_logging():
    _setup_logging()
    return True