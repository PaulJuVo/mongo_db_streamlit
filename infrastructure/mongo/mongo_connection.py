from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from config.mongo_config import APPUSER_URI, DASHBOARDUSER_URI, MongoUser
import logging
logger = logging.getLogger("mongo")

class MongoConnection:
    

    def __init__(self, user : MongoUser):
        self.user = user
        self.connected = False

    def connect(self):
        if self.user == MongoUser.APPUSER:
            self.uri = APPUSER_URI
        elif self.user == MongoUser.DASHBOARDUSER:
            self.uri = DASHBOARDUSER_URI
        else:
            raise ValueError(f"{self.user} has no connection String in Mongo Config File")
        
        try:
            self.client = MongoClient(self.uri)
            self.client.server_info() 
            self.connected = True
            logger.info(f"--- Connected as {self.user.value} ---")
        except ServerSelectionTimeoutError:
            logger.exception(f"Not able to connect to database {self.user.value}\
                             \n {self.uri}")
            raise
        

    def close(self):
        self.client.close()
        self.connected = False
        logger.info(f"--- Connection closed: {self.user.value} ---")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        
            