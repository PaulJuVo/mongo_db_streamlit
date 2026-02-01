'''
extract data from zip
- unpack zip
- choose right jsons

load to mongoDB/raw
'''
import zipfile
import pathlib


# TODO delete imports für DIP

from config.mongo_config import MongoCollection, MongoDatabase, MongoUser
from core.ports.base_repository_interface import BaseRepositoryInterface
from infrastructure.mongo.mongo_connection import MongoConnection
from infrastructure.mongo.mongo_repository import MongoRepository
from core.domain.extract import run_import as test
import logging

logger = logging.getLogger(__name__)

def run_import(zip_path : pathlib.Path):
    with zipfile.ZipFile(zip_path) as zip_ref:
        zip_ref.printdir()


def test_dependency_injection(uow : BaseRepositoryInterface):
    assert uow is not None, "eodPrice Repository wurde nicht gesetzt!"
    logger.warning("logger is aktiv")
    uow.execute()
    
    


if __name__ == "__main__":
    from config.logging_config import setup_logging
    
    setup_logging()
    test()
    path_zip = pathlib.Path("/Users/paulvogt/mongo_db_streamlit/tmp/raw/SP_2026-01-09.zip")
    # run_import(path_zip)
    with MongoConnection(MongoUser.APPUSER) as conn:
        raw_db_test = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.TEST)
        raw_eod = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.EODPRICE)
        processed_tets = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.TEST)
        test_dependency_injection(raw_db_test)
        test_dependency_injection(raw_eod)
        test_dependency_injection(processed_tets)