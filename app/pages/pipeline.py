import os
import streamlit as st
from infrastructure.mongo.mongo_repository import MongoRepository
from config.mongo_config import MongoCollection, MongoDatabase, MongoUser
from app.shared.logging import init_logging
from app.shared.mongo import get_mongo
from core.application.run_import import import_many, import_constituents,import_sp500, import_spxew
from core.application.pipeline_service import PipelineService
from core.exceptions.dashboard_exceptions import EmptyJson
from core.application.notification_service import notify
import time
import logging
from pathlib import Path
from typing import Optional
import ijson
import json

init_logging()
logger = logging.getLogger("Streamlit - Pipeline")

st.title("Pipeline", text_alignment="center")
def get_dict_from_json(rawJson, collection_name: Optional[str] = None):
    # Sonderfall: ganzes Objekt (kein Array auf top-level)
    is_single_object = (
        collection_name == MongoCollection.EODPRICE.value.lower() or
        collection_name in [MongoCollection.SP500.value, MongoCollection.SPXEW.value]
    )

    if is_single_object:
        data = json.load(rawJson)
        if not data:
            raise EmptyJson("is empty")
        yield data
    else:
        # JSON-Array → record by record streamen, nie alles im RAM
        found_any = False
        for record in ijson.items(rawJson, "item"):  # "item" = jedes Element des top-level Arrays
            found_any = True
            yield record
        if not found_any:
            raise EmptyJson("is empty")

from decimal import Decimal

def normalize_types(obj):
    if isinstance(obj, dict):
        return {k: normalize_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [normalize_types(v) for v in obj]
    elif isinstance(obj, Decimal):
        return float(obj)  # oder Decimal128
    return obj


def import_files(upload_file):
    i = 0
    size = len(upload_file)
    msg = "Import process finished"
    failed_import_counter = 0

    if size < 1:
        st.toast("There is nothing to Import", icon="🤠")
        return

    pg_bar = st.progress(i / size, "Importing files")
    mapped_data = {}
    BATCH_SIZE = 500

    for file in upload_file:
        try:
            coll_name = get_collection_name(file)
            repo = get_repo(coll_name)

            with open(file) as ofile:
                for record in get_dict_from_json(ofile, coll_name): 
                    mapped_data.setdefault(repo, []).append(normalize_types(record))

                    if len(mapped_data[repo]) >= BATCH_SIZE:
                        import_many(repo, mapped_data[repo])
                        mapped_data[repo].clear()  # ← Speicher sofort freigeben

        except Exception as e:
            if isinstance(e, EmptyJson):
                logger.warning(f"Couldn't import {file}: {e}")
            else:
                logger.info(f"Couldn't import {file}: {e}")
            failed_import_counter += 1
        finally:
            i += 1
            pg_bar.progress(i / size, "Importing JSON Files")

    for repo, remaining in mapped_data.items():
        if remaining:
            import_many(repo, remaining)
            remaining.clear()  # ← explizit freigeben

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

def get_collection_name(rawJson):
    # rawJson kann Path oder UploadedFile sein

    rawpath = Path(rawJson).resolve()   # sicherstellen, dass es Path ist
    rawname = rawpath.name

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

def _import_file(path: Path, collection_name: Optional[str], import_fn, repo):
    fname = str(path)
    try:
        with open(path) as file:
            fname = file.name
            data = get_dict_from_json(file, collection_name)
            import_fn(repo, data)
    except FileNotFoundError:
        logger.warning(f"File not found: {fname}")
    except Exception as e:
        logger.warning(f"Couldn't import {fname}: {e}")

def import_constituent():
    _import_file(CONSTITUENTS_PATH, None, import_constituents, constituents_repo)

def import_sp_data():
    _import_file(SP_500_PATH, MongoCollection.SP500.value, import_sp500, sp500_raw_repo)

def import_spxew_data():
    _import_file(SPXEW_PATH, MongoCollection.SPXEW.value, import_spxew, spxew_raw_repo)
     
def chunked(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

DATA_PATH = Path(os.environ.get("DATA_PATH", Path(__file__).parent.parent.parent / "data"))

CONSTITUENTS_PATH = DATA_PATH / "0_sp_500_constituents_historical_2026.json"
SP_500_PATH       = DATA_PATH / "^GSPC_eod_prices.json"
SPXEW_PATH        = DATA_PATH / "^SPXEW_autoadjusted.json"
RAW_DATA          = DATA_PATH / "data"


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
const_wiki_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.CONST_WIKI)
const_wiki_changes_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.CONST_WIKI_CHANGES)


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
                                    const_wiki_repo=const_wiki_repo,
                                    const_wiki_changes_repo=const_wiki_changes_repo
                                    )


col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button(label="Run Import & Pipeline", icon="🚀", use_container_width=True, help="Startet den kompletten ETL-Prozess"):
        with st.spinner("Pipeline läuft...", show_time=True):
            
            st.write("📥 **Import**")
            notify("Started Import")
            start_time = time.time()
            
            import_constituent()
            
            import_spxew_data()
            
            import_sp_data()
            
            files = list(RAW_DATA.glob("*.json"))
            import_files(upload_file=files)
            
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

    if st.button(label="Run Pipeline", icon="⚡️", use_container_width=True, help="Startet den Pipeline-Prozess"):
        with st.spinner("Pipeline läuft...", show_time=True):
            st.write("⚙️ **Pipeline**")
            pipe_progress = st.progress(0, text="Pipeline wird ausgeführt...")
            pipe_start = time.time()
            
            pipeline_service.run()
            
            pipe_time = time.time() - pipe_start
            pipe_progress.progress(100, text="Pipeline abgeschlossen ✅")
            st.success(f"Pipeline abgeschlossen in {pipe_time / 60:.1f} min")

        st.toast("Pipeline run completed ✅")
                     


                
          




    
    


