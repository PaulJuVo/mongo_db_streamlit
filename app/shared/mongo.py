from infrastructure.mongo.mongo_connection import MongoConnection
from config.mongo_config import MongoUser, MongoCollection, MongoDatabase
import streamlit as st

@st.cache_resource
def get_mongo(user : MongoUser):
    conn = MongoConnection(user)
    conn.connect()
    return conn
