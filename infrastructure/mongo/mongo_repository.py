from core.ports.base_repository_interface import BaseRepositoryInterface
from infrastructure.mongo.mongo_connection import MongoConnection
from config.mongo_config import MongoDatabase, MongoCollection
from config.logging_config import performance_log
import logging


class MongoRepository(BaseRepositoryInterface):
    logger = logging.getLogger("mongo")
    def __init__(self, mongo_connection : MongoConnection, db : MongoDatabase, collection : MongoCollection):
        self.mongo_connection = mongo_connection
        self.db = mongo_connection.client.get_database(db.value)
        self.collection = self.db.get_collection(collection.value)
     
    @performance_log(logger)
    def execute(self):
        self.collection.insert_one({"x": 77})
        return None
    
    @performance_log(logger)
    def exists(self, filter):
        rec = self.collection.find_one(filter=filter)
        return rec is not None
    
    @performance_log(logger)
    def insert_one(self, data):
        return self.collection.insert_one(data)
    
    @performance_log(logger)
    def insert_many(self, data):
        return self.collection.insert_many(data)

    def find_all(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError
    
    def get_collection_name(self):
        return self.collection.name
    
    def delete(self, filter):
        self.collection.delete_many(filter=filter)
