import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
from infrastructure.mongo.mongo_repository import MongoRepository
from config.mongo_config import MongoCollection, MongoDatabase, MongoUser
from app.shared.logging import init_logging
from app.shared.mongo import get_mongo
from core.application.run_import import import_many
from app.adapter.adapter import get_dict_from_json
from core.application.etl_pipeline import PipelineService
import time
import logging



init_logging()
logger = logging.getLogger("Streamlit - Pipeline")

st.title("Pipeline")

def import_files(upload_file):
    i = 0 
    size = len(upload_file)
    msg = "Import process finished" 
    failed_import_counter = 0
    if size < 1:
        st.toast("There is nothing to Import", icon="🤠")
        return
    pg_bar = st.progress(i / size, "Importing files")
    for file in upload_file:
        try:
            coll_name = get_collection_name(file)
            data = get_dict_from_json(file, coll_name)
            
            if coll_name == MongoCollection.PROFILE.value.lower():
                repo = profile_repo
            elif coll_name == MongoCollection.INCOMESTATEMENT.value.lower():
                repo = income_repo
            else: # coll_name =="eodprices"
                repo = eod_repo
            import_many(repo, data)
        except Exception as e:
            st.toast(f"Couldn't import {file.name}: {e}", icon="❌", duration="short")
            failed_import_counter += 1
            continue
        finally:
            i += 1
            pg_bar.progress(i / size)
            
    if failed_import_counter > 0:
        msg += f" but {failed_import_counter} files couldn't get imported"
    pg_bar.empty()
    st.toast(f"{msg}", icon="☑️")
    
        
     
def get_collection_name(rawJson : UploadedFile):
    name : str = rawJson.name
    name = name.removesuffix(".json")
    parts = name.split("_", 1)
    if len(parts) != 2:
        raise ValueError(f"Ungültiger Dateiname: {name}")
    normalized = parts[1].lower().replace("_", "")
    if normalized == "eodprices":
        normalized = "eodprice"
    if normalized in [c.value.lower() for c in MongoCollection]:
        return normalized
    else:
        raise ValueError(f"Keine gemappte Mongo Collection für: {name}")

conn = get_mongo(MongoUser.APPUSER)
eod_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.EODPRICE)
staged_eod_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.STAGED_EODPRICE)
staged_income_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.STAGED_INCOMESTATEMENT)
income_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.INCOMESTATEMENT)
profile_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.PROFILE)

pipeline = PipelineService(eodprice_repo=eod_repo, 
                           income_repo=income_repo, 
                           profile_repo=profile_repo, 
                           staged_income_repo=staged_income_repo, 
                           staged_eodprice_repo=staged_eod_repo)

upload_container = st.container()
container = st.container(horizontal=True, horizontal_alignment="left")


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
        
if st.button(label="Run pipeline", icon="🚀", icon_position="right", help="run etl pipeline"):
    with st.spinner("running Pipeline...", show_time=True):
        pipeline.run() 
    st.toast(f"Pipeline run completed", icon="✅", duration="long")
                
                     


                
          




    
    


