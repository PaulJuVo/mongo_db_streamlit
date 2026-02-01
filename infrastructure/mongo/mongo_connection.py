from pymongo import MongoClient, errors
from pymongo.errors import ServerSelectionTimeoutError

class Mongo_Connection:
    def __init__(self, user, password, host, port, db_name):
        self.user = user
        self.password = password
        self.connected = False
        self.host = host
        self.port = port
        self.db_name = db_name
        self.db = None
        self.connected = False

    def connect(self):
        conn_str = f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}?authSource={self.db_name}"
        self.client = MongoClient(conn_str)
    
        try:
            self.client.server_info()
            self.db = self.client[self.db_name]  
            self.connected = True
            print(f"--- Connected as {self.user} ---")
        except ServerSelectionTimeoutError as e:
            print(f"Not able to connect to database")
            print(f"Error: {e}")
        
    
    def get_db(self):
        return self.client[self.db_name]

    def close(self):
        self.client.close()
        self.connected = False
        print(f"--- Connection {self.user} closed ---")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        
            