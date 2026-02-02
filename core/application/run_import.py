'''
extract data from zip
- unpack zip
- choose right jsons

load to mongoDB/raw
'''
import zipfile
import pathlib


# TODO delete imports für DIP


from core.ports.base_repository_interface import BaseRepositoryInterface
from core.domain.extract import run_import as test
import logging

logger = logging.getLogger(__name__)

def run_import(zip_path : pathlib.Path):
    with zipfile.ZipFile(zip_path) as zip_ref:
        zip_ref.printdir()


def test_dependency_injection(uow : BaseRepositoryInterface):
    assert uow is not None, "eodPrice Repository wurde nicht gesetzt!"
    logger.info("dip ist aktiv und funktioniert")
    uow.execute()

def test_ui_connection():
    logger.info("UI Connected")
    return "Test complete"
    


if __name__ == "__main__":
    
    test()
    path_zip = pathlib.Path("/Users/paulvogt/mongo_db_streamlit/tmp/raw/SP_2026-01-09.zip")
    # run_import(path_zip)
   