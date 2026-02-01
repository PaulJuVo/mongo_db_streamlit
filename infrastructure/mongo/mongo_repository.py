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
        print(self.collection.name)
        self.collection.insert_one({"x": 69})
        return None

    def find_all(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError