import streamlit as st
from core.application.run_import import test_ui_connection, test_dependency_injection
from config.logging_config import setup_logging
from infrastructure.mongo.mongo_connection import MongoConnection
from infrastructure.mongo.mongo_repository import MongoRepository
from config.mongo_config import MongoCollection, MongoDatabase, MongoUser

@st.cache_resource   
def log():
    setup_logging()
log()

st.title("Mein Dashboard Mona M")
st.write(test_ui_connection())

@st.cache_resource
def get_mongo():
    conn = MongoConnection(MongoUser.APPUSER)
    conn.connect()
    return conn

conn = get_mongo()

repo = MongoRepository(mongo_connection=conn, db=MongoDatabase.PROCESSED, collection=MongoCollection.TEST)
test_dependency_injection(repo)

upload_file = st.file_uploader(label="Upload zip", 
                               type="json", 
                               accept_multiple_files='directory', 
                               max_upload_size=2000)

if upload_file:
    st.info("upload sucseded")


