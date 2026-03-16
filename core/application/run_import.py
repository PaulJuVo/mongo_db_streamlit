from core.ports.base_repository_interface import BaseRepositoryInterface
from config.logging_config import performance_log
from config.mongo_config import FILTER_QUERIES_UPLOAD
from config.processed_schema import VALIDATION_SCHEMAS
from jsonschema import validate, ValidationError
import datetime 
import logging

logger = logging.getLogger(__name__)

@performance_log(logger)
def import_many(repo: BaseRepositoryInterface, data : list[dict]):
    collection_name = repo.get_collection_name()
    filter_queries = FILTER_QUERIES_UPLOAD[collection_name]
    schema = VALIDATION_SCHEMAS[collection_name]
    insert_data = []
    rejected_data = []

    for each in data:
        try:
            validate(instance=each, schema=schema)
            insert_data.append(each)
        except ValidationError as e :
            logger.warning(f"{collection_name} Upload data was rejected: {e.message}")
            rejected_data.append({**each, "rejectionTime": datetime.datetime.now(), "validationError": e.message})
            continue

    if insert_data:
        # filter collections for unique identifier like symbol and/or date to delete old records
        all_filters = [
            {k: each[k] for key in each.keys() for k in filter_queries if key == k}
            for each in insert_data
        ]
        for i in range(0, len(all_filters), 1000):
            repo.delete({"$or": all_filters[i:i + 1000]})
        repo.insert_many(insert_data)
    repo.write_rejected_data(rejected_data)

def import_constituents(repo: BaseRepositoryInterface, data : list[dict]):
    try:
        repo.drop()
        repo.insert_many(data)
    except Exception:
        raise

def import_sp500(repo: BaseRepositoryInterface, data : list[dict]):
    try:
        repo.drop()
        repo.insert_many(data)
    except Exception:
        raise

def import_spxew(repo: BaseRepositoryInterface, data : list[dict]):
    try:
        repo.drop()
        repo.insert_many(data)
    except Exception:
        raise