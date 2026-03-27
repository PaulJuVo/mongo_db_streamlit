from typing import Any
from core.interfaces.base_repository_interface import BaseRepositoryInterface
from core.interfaces.cursor import Cursor
from infrastructure.mongo.mongo_connection import MongoConnection
from config.mongo_config import MongoDatabase, MongoCollection
from config.logging_config import performance_log
from pymongo import UpdateOne
import logging


class MongoRepository(BaseRepositoryInterface):
    logger = logging.getLogger("mongo")
    def __init__(self, mongo_connection : MongoConnection, db : MongoDatabase, collection : MongoCollection):
        self.mongo_connection = mongo_connection
        self.db = mongo_connection.client.get_database(db.value)
        self.collection = self.db.get_collection(collection.value)
        self.rejection_collection = self.collection.name + "_rejected"
    
    def insert_many(self, data):
        if data:
            self.collection.insert_many(data)
    
    def get_collection_name(self):
        return self.collection.name
    
    def delete(self, filter):
        self.collection.delete_many(filter=filter)
    
    def drop(self):
        self.db.drop_collection(self.collection)

    def create_time_series(self, config):
        name = self.collection.name
        self.db.create_collection(name,timeseries=config)
    
    def write_rejected_data(self, data):
        if data:
            self.db[self.rejection_collection].insert_many(data)
    
    @performance_log(logger)
    def execute_pipeline(self, pipeline):
        return self.collection.aggregate(pipeline)
    
    def find(self, filter = None, batch_size = 101, limit = 0, projection = None, sort = None) -> Cursor[dict]:
        return self.collection.find(filter = filter, batch_size = batch_size, limit = limit, projection = projection, sort = sort)
    
    def find_one(self, filter = None, sort = None) -> Any:
        return self.collection.find_one(filter = filter, sort = sort)
    
    def find_distinct(self,key, filter = None)  -> list[Any]:
        return self.collection.distinct(key=key, filter = filter)

    def create_index(self, keys : list[tuple], unique : bool):
        self.collection.create_index(keys=keys, unique=unique)

    def upsert_one(self, filter, update):
        return self.collection.update_one(filter=filter, update=update, upsert=True)

    def bulk_write(self, operations):
        self.collection.bulk_write(operations)

    def make_upsert(self, doc):
        from pymongo import UpdateOne
        return UpdateOne(
        {"symbol": doc["symbol"], "date": doc["date"]},
        {"$set": doc},
        upsert=True
        )
