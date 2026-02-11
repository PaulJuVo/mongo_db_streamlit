from core.ports.base_repository_interface import BaseRepositoryInterface
from infrastructure.mongo.mongo_connection import MongoConnection
from config.mongo_config import MongoDatabase, MongoCollection
from config.logging_config import performance_log
from pymongo import errors
import logging


class MongoRepository(BaseRepositoryInterface):
    logger = logging.getLogger("mongo")
    def __init__(self, mongo_connection : MongoConnection, db : MongoDatabase, collection : MongoCollection):
        self.mongo_connection = mongo_connection
        self.db = mongo_connection.client.get_database(db.value)
        self.collection = self.db.get_collection(collection.value)
        self.rejection_collection = self.collection.name + "_rejected"
    
    def insert_one(self, data):
        return self.collection.insert_one(data)
    
    @performance_log(logger)
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
        try:
            cursor = self.collection.aggregate(pipeline)
            results = list(cursor)
            return results
        except errors.PyMongoError as e:
            self.logger.exception("Fehler bei aggregate(): %s", e)
            raise
    @performance_log(logger)
    def run_db_command(self, command):
        self.db.command(command)
