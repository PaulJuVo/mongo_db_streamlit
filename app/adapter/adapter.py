from config.mongo_config import MongoCollection
import json
from streamlit.runtime.uploaded_file_manager import UploadedFile
from itertools import count
from typing import Iterable


def _to_profile(data : list[dict]):
    return data

def _to_income_statement(data : list[dict]):
    return data

def _to_eod_prices(data : dict):
    return [{"symbol": data["symbol"], **rec} for rec in data["historical"]]
     
def get_dict_from_json(rawJson : UploadedFile, collection_name):
    data = json.load(rawJson)
    data_dict = []
    print(f"------ ----- ----- {collection_name}")
    _check_empty(data)
    match collection_name:
        case "profile":
            data_dict = _to_profile(data)
        case "incomestatement":
            data_dict = _to_income_statement(data)
        case "eod_prices":
            data_dict = _to_eod_prices(data)
        case _:
            raise ValueError("could not resolve collection_name")
    return data_dict

def _check_empty(data : Iterable):
    if not data:
       raise ValueError(f"is empty")

