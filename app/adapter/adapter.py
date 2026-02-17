from config.mongo_config import MongoCollection
import json
from streamlit.runtime.uploaded_file_manager import UploadedFile

def get_dict_from_json(rawJson, collection_name):
    data = json.load(rawJson)
    data_dict = []
    if not data:
       raise ValueError(f"is empty")
    if collection_name == MongoCollection.EODPRICE.value.lower():
        data_dict = [data]
    else:
        data_dict = data
    return data_dict

    

