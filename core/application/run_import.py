from core.ports.base_repository_interface import BaseRepositoryInterface
from config.mongo_config import FILTER_QUERIES_UPLOAD
from config.logging_config import performance_log
import logging
import json
from pprint import pprint

logger = logging.getLogger(__name__)

@performance_log(logger)
def import_many(repo: BaseRepositoryInterface, data : list[dict]):
    collection_name = repo.get_collection_name()
    filter_queries = FILTER_QUERIES_UPLOAD[collection_name]
    insert_data = []
    try:
        for each in data:
            filter = { k : each[k] for key in each.keys() for k in filter_queries if key == k }
            repo.delete(filter)
            insert_data.append(each)
        repo.insert_many(insert_data)
    except Exception:
        logger.exception("Import not working")
        raise