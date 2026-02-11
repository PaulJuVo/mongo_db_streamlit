import streamlit as st
from infrastructure.mongo.mongo_connection import MongoConnection
from infrastructure.mongo.mongo_repository import MongoRepository
from config.mongo_config import MongoCollection, MongoDatabase, MongoUser
from app.shared.logging import init_logging
from app.shared.mongo import get_mongo
from config.pipeline_config import COMPANY_PIPELINE, STAGED_FINANCEDATA_PIPELINE
from core.application.run_etl_pipeline import run_pipeline
import logging



init_logging()
logger = logging.getLogger("Streamlit - Upload")

st.title("Transformations")
conn = get_mongo(MongoUser.APPUSER)
repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.EODPRICE)

if st.button(label="Run pipeline", icon="🚀", 
              icon_position="right", help="run etl pipeline"):
    run_pipeline(repo, STAGED_FINANCEDATA_PIPELINE)