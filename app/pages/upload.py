from typing import List
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
from infrastructure.mongo.mongo_connection import MongoConnection
from infrastructure.mongo.mongo_repository import MongoRepository
from config.mongo_config import MongoCollection, MongoDatabase, MongoUser
from app.shared.logging import init_logging
from app.shared.mongo import get_mongo
from core.application.run_import import import_many
from app.adapter.adapter import get_dict_from_json
import logging



init_logging()
logger = logging.getLogger("Streamli - Upload")

st.title("Upload")

def import_files(upload_file):
    i = 0 
    size = len(upload_file)
    if size < 1:
        st.toast("There is nothing to Import", icon="🤠")
        return
    pg_bar = st.progress(i / size, "Importing files")
    for file in upload_file:
        try:
            coll_name = get_collection_name(file)
            data = get_dict_from_json(file, coll_name)
            if coll_name == "profile":
                repo = profile_repo
            elif coll_name == "incomestatement":
                repo = income_repo
            else: # coll_name =="eod_prices"
                repo = eod_repo
            import_many(repo, data)
        except Exception as e:
             logger.exception("Could not import")
             st.toast(f"Couldn't import {file.name}: {e}", icon="❌", duration="short")
             continue
        finally:
            i += 1
            pg_bar.progress(i / size)
            
    pg_bar.empty()
    st.success("Import completed")  
        

     
def get_collection_name(rawJson : UploadedFile):
    name : str = rawJson.name
    name = name.removesuffix(".json")
    collection_name = name.split("_", maxsplit=1)[1].lower()
    return collection_name

conn = get_mongo(MongoUser.APPUSER)
eod_repo = MongoRepository(mongo_connection=conn, db=MongoDatabase.RAW, collection=MongoCollection.EODPRICE)
income_repo = MongoRepository(mongo_connection=conn, db=MongoDatabase.RAW, collection=MongoCollection.INCOMESTATEMENT)
profile_repo = MongoRepository(mongo_connection=conn, db=MongoDatabase.RAW, collection=MongoCollection.PROFILE)

container = st.container(horizontal=True, horizontal_alignment="left")
upload_container = st.container()

with upload_container:
    upload_file: list[UploadedFile] = upload_container.file_uploader(label="Upload JSON or directory with JSON", 
                               type="json", 
                               accept_multiple_files='directory', 
                               max_upload_size=2000)
         
with container:
     if st.button(label="Import to Database", icon="💾", 
              icon_position="right", help="Import the data to the MongoDb Database"):
        with st.spinner("Importing Files", show_time=True):
            import_files(upload_file=upload_file)
            
           

                
                     
                
          




    
    


