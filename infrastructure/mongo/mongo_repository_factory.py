import os
from dotenv import load_dotenv
from infrastructure.mongo.mongo_unit_of_work import MongoUnitOfWork
from infrastructure.mongo.mongo_connection import Mongo_Connection
from contextlib import contextmanager
from infrastructure.mongo.mongo_user import Mongo_user
from config.mongo_config import USER_CONFIG

class Mongo_Repository_factory():
    @staticmethod
    @contextmanager
    def get_uow(db_user : Mongo_user):
        # TODO für prod ready machen
        load_dotenv(".env.dev")
        host = os.environ["MONGO_HOST"]
        port = os.environ["MONGO_PORT"]
    
        if db_user not in USER_CONFIG:
            raise ValueError("DB User does not exist")

        config = USER_CONFIG[db_user]

        user = os.environ[config["user"]]
        password = os.environ[config["password"]]
        db_name = os.environ[config["db"]]
            
        with Mongo_Connection(user, password, host, port, db_name) as conn:
            with MongoUnitOfWork(conn, db_user) as uow:
                yield uow



