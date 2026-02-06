import streamlit as st
from config.logging_config import setup_logging
from infrastructure.mongo.mongo_connection import MongoConnection
from infrastructure.mongo.mongo_repository import MongoRepository
from config.mongo_config import MongoCollection, MongoDatabase, MongoUser


st.title("Hallo")


