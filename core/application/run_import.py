from core.ports.base_repository_interface import BaseRepositoryInterface
from config.logging_config import performance_log
from config.mongo_config import FILTER_QUERIES_UPLOAD
from config.processed_schema import VALIDATION_SCHEMAS
from jsonschema import validate, ValidationError
import datetime 
import logging

# TODO eigene exceptions

logger = logging.getLogger(__name__)

@performance_log(logger)
def import_many(repo: BaseRepositoryInterface, data : list[dict]):
    collection_name = repo.get_collection_name()
    filter_queries = FILTER_QUERIES_UPLOAD[collection_name]
    schema = VALIDATION_SCHEMAS[collection_name]
    insert_data = []
    rejected_data = []
    # TODO Upsert anstatt delete and insertmany.. außer wenn kompletter batch importiert werden soll.
    try:
        for each in data:
            # filter collections for unique identifier like symbol and/or date to delete old records
            filter = { k : each[k] for key in each.keys() for k in filter_queries if key == k }
            try:
                validate(instance=each, schema=schema)
                repo.delete(filter)
                insert_data.append(each)
            except ValidationError as e :
                logger.warning(f"{collection_name} Upload data was rejected: {e.message}")
                rejected_data.append({**each, "rejectionTime": datetime.datetime.now(), "validationError": e.message})
                continue
        repo.insert_many(insert_data)
        repo.write_rejected_data(rejected_data)
    except Exception:
        raise

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