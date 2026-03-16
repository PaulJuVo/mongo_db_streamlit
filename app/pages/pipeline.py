import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
from infrastructure.mongo.mongo_repository import MongoRepository
from config.mongo_config import MongoCollection, MongoDatabase, MongoUser
from app.shared.logging import init_logging
from app.shared.mongo import get_mongo
from core.application.run_import import import_many, import_constituents,import_sp500, import_spxew
from app.adapter.adapter import get_dict_from_json
from core.application.pipeline_service import PipelineService
from core.exceptions.dashboard_exceptions import EmptyJson
from core.application.notification_service import notify
import time
import logging
from pathlib import Path

init_logging()
logger = logging.getLogger("Streamlit - Pipeline")

st.title("Pipeline", text_alignment="center")

def import_files(upload_file, is_path = False):
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
            if is_path:
                with open(file) as ofile:
                    coll_name = get_collection_name(ofile, is_path=is_path)
                    repo = get_repo(coll_name)
                    data = get_dict_from_json(ofile, coll_name)
            else:
                coll_name = get_collection_name(file, is_path=is_path)
                repo = get_repo(coll_name)
                data = get_dict_from_json(file, coll_name)
            import_many(repo, data)
        except Exception as e:
            if isinstance(e, EmptyJson):
                logger.warning(f"Couldn't import {file.name}: {e}")
            logger.info(f"Couldn't import {file.name}: {e}")
            failed_import_counter += 1
            continue
        finally:
            i += 1
            pg_bar.progress(i / size)
            
    if failed_import_counter > 0:
        msg += f" but {failed_import_counter} files couldn't get imported"
    pg_bar.empty()
    st.toast(f"{msg}", icon="☑️")

def get_repo(collection_name):
    if collection_name == MongoCollection.PROFILE.value.lower():
                repo = profile_repo
    elif collection_name == MongoCollection.INCOMESTATEMENT.value.lower():
            repo = income_repo
    elif collection_name == MongoCollection.EODPRICE.value.lower():
            repo = eod_repo
    elif collection_name == MongoCollection.CASHFLOW.value.lower():
            repo = cashflow_repo
    else:
        raise ValueError(f"Keine gemappte Mongo Collection für: {collection_name}")
    return repo

def get_collection_name(rawJson, is_path : bool):
    rawname : str = rawJson.name
    if is_path:
        rawname = Path(rawname).resolve().relative_to(PROJECT_ROOT).name
    name = rawname.removesuffix(".json")
    coll_name = map_filename_to_collection(name)
    return coll_name

def map_filename_to_collection(name):
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

def import_constituent():
    try:
        with open(CONSTITUENTS_PATH) as file:
            data = get_dict_from_json(file)
            import_constituents(constituents_repo, data)
    except Exception as e:
        logger.warning(f"Couldn't import {file.name}: {e}")

def import_sp_data():
    try:
        with open(SP_500_PATH) as file:
            data = get_dict_from_json(file, MongoCollection.SP500.value)
            import_sp500(sp500_raw_repo, data)
    except Exception as e:
        logger.warning(f"Couldn't import {file.name}: {e}")

def import_spxew_data():
    try:
        with open(SPXEW_PATH) as file:
            data = get_dict_from_json(file, MongoCollection.SPXEW.value)
            import_spxew(spxew_raw_repo, data)
    except Exception as e:
        logger.warning(f"Couldn't import {file.name}: {e}")
     


FILE = Path(__file__).resolve()
PROJECT_ROOT = FILE.parents[2]
DATA_PATH = PROJECT_ROOT / "tmp" / "data"
CONSTITUENTS_PATH = PROJECT_ROOT / "tmp" / "0_sp_500_constituents_historical_2026.json"
SP_500_PATH = PROJECT_ROOT / "tmp" / "^GSPC_eod_prices.json"
SPXEW_PATH = PROJECT_ROOT / "tmp" / "^SPXEW_autoadjusted.json"


conn = get_mongo(MongoUser.APPUSER)

constituents_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.CONSTITUENTS)
scd_constituents_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.SCD_CONSTITUENTS)
sector_repo =  MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.SECTORDATA)
sp500_raw_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.SP500)
spxew_raw_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.SPXEW)
sp500_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.SP500)
finance_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.FINANCEDATA)
company_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.COMPANYDATA)
eod_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.EODPRICE)
cashflow_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.CASHFLOW)
staged_eod_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.STAGED_EODPRICE)
staged_income_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.STAGED_INCOMESTATEMENT)
staged_cashflow_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.STAGED_CASHFLOW)
income_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.INCOMESTATEMENT)
profile_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.PROFILE)
pipeline_service = PipelineService(eodprice_repo=eod_repo, 
                                    income_repo=income_repo,
                                    cashflow_repo=cashflow_repo, 
                                    staged_eodprice_repo=staged_eod_repo, 
                                    staged_income_repo=staged_income_repo,
                                    staged_cashflow_repo=staged_cashflow_repo, 
                                    profile_repo=profile_repo, 
                                    financedata_repo=finance_repo, 
                                    company_repo=company_repo,
                                    constituents_repo=constituents_repo,
                                    scd_constituents_repo=scd_constituents_repo,
                                    sector_repo = sector_repo,
                                    sp500_raw_repo=sp500_raw_repo,
                                    sp500_repo=sp500_repo,
                                    )



###         
### if st.button(label="Run Import and Pipeline", icon="🚀", icon_position="right", help="run etl pipeline"):
###     with st.spinner("running Pipeline...", show_time=True):
###         notify("Started Import")
###         start_time = time.time()
###         import_constituent()
###         import_spxew_data()
###         import_sp_data()
### 
###         files = []
###         json_files = list(DATA_PATH.glob("*.json"))
###         for file in json_files:
###             files.append(file)
###         import_files(upload_file=files, is_path=True)
###         imp_time = time.time() - start_time
###         notify(f"Import finished with {imp_time / 60:.0f} min")
###     
###         pipe_start = time.time()
###         pipeline_service.run()
###         pipe_time = time.time() - pipe_start 
###         notify(f"Pipeline finished with {pipe_time / 60:.0f} min")
###     st.toast(f"Pipeline run completed", icon="✅", duration="long")


col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button(label="Run Import & Pipeline", icon="🚀", use_container_width=True, help="Startet den kompletten ETL-Prozess"):
        with st.spinner("Pipeline läuft...", show_time=True):
            
            st.write("📥 **Import**")
            progress = st.progress(0, text="Constituents werden importiert...")
            notify("Started Import")
            start_time = time.time()
            
            import_constituent()
            progress.progress(25, text="SPXEW Daten werden importiert...")
            
            import_spxew_data()
            progress.progress(50, text="SP500 Daten werden importiert...")
            
            import_sp_data()
            progress.progress(75, text="JSON Files werden importiert...")
            
            files = list(DATA_PATH.glob("*.json"))
            import_files(upload_file=files, is_path=True)
            progress.progress(100, text="Import abgeschlossen ✅")
            
            imp_time = time.time() - start_time
            notify(f"Import finished with {imp_time / 60:.0f} min")
            st.success(f"Import abgeschlossen in {imp_time / 60:.1f} min")

            st.write("⚙️ **Pipeline**")
            pipe_progress = st.progress(0, text="Pipeline wird ausgeführt...")
            pipe_start = time.time()
            
            pipeline_service.run()
            
            pipe_time = time.time() - pipe_start
            pipe_progress.progress(100, text="Pipeline abgeschlossen ✅")
            notify(f"Pipeline finished with {pipe_time / 60:.0f} min")
            st.success(f"Pipeline abgeschlossen in {pipe_time / 60:.1f} min")

        st.toast("Pipeline run completed ✅")
                
                     


                
          




    
    


