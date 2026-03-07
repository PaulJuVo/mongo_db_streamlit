from typing import Optional
from config.mongo_config import MongoCollection
from core.exceptions.dashboard_exceptions import EmptyJson
import json

def get_dict_from_json(rawJson, collection_name : Optional[str] = None):
    data = json.load(rawJson)
    data_dict = []
    if not data:
       raise EmptyJson(f"is empty")
    if collection_name == MongoCollection.EODPRICE.value.lower() or collection_name in [MongoCollection.SP500.value, MongoCollection.SPXEW.value]:
        data_dict = [data]
    else:
        data_dict = data
    return data_dict

    

