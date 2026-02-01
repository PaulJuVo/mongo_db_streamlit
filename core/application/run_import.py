'''
extract data from zip
- unpack zip
- choose right jsons

load to mongoDB/raw
'''
import zipfile
import pathlib
from core.ports.unit_of_work_interface import unit_of_work_interface

# TODO delete imports für DIP
from infrastructure.mongo.mongo_repository_factory import Mongo_Repository_factory as mongo_fac
from infrastructure.mongo.mongo_user import Mongo_user 

def run_import(zip_path : pathlib.Path):
    with zipfile.ZipFile(zip_path) as zip_ref:
        zip_ref.printdir()


def test_dependency_injection(uow : unit_of_work_interface):
    assert uow.eodPrice is not None, "eodPrice Repository wurde nicht gesetzt!"
    uow.eodPrice.execute("hello")
    


if __name__ == "__main__":
    path_zip = pathlib.Path("/Users/paulvogt/mongo_db_streamlit/tmp/raw/SP_2026-01-09.zip")
    # run_import(path_zip)
    with mongo_fac.get_uow(Mongo_user.PROCESSEDUSER) as uow:
        test_dependency_injection(uow)