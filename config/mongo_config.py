from enum import Enum
import os

class MongoUser(Enum):
    APPUSER = "appUser"
    DASHBOARDUSER = "dashboardUser"

class MongoDatabase(Enum):
    RAW = "raw"
    PROCESSED = "processed"

class MongoCollection(Enum):
    EODPRICE = "eodPrice"
    TEST = "test"

# DEPRICATED
USER_CONFIG = {
    MongoUser.APPUSER: {
        "user": "MONGO_APPUSER_USER",
        "password": "MONGO_APPUSER_PASSWORD",
        "auth_db": "MONGO_APPUSER_AUTH_DB",
    },
    MongoUser.DASHBOARDUSER: {
        "user": "MONGO_DASHBOARDUSER_USER",
        "password": "MONGO_DASHBOARDUSER_PASSWORD",
        "auth_db": "MONGO_DASHBOARDUSER_AUTH_DB",
    }
}

from dotenv import load_dotenv
load_dotenv(".env.dev")

HOST = os.environ["MONGO_HOST"]
PORT = os.environ["MONGO_PORT"]

APPUSER_USER = os.environ["MONGO_APPUSER_USER"]
APPUSER_PASSWORD = os.environ["MONGO_APPUSER_PASSWORD"]
APPUSER_AUTHDB = os.environ["MONGO_APPUSER_AUTH_DB"]

DASHBOARDUSER_USER = os.environ["MONGO_DASHBOARDUSER_USER"]
DASHBOARDUSER_PASSWORD = os.environ["MONGO_DASHBOARDUSER_PASSWORD"]
DASHBOARDUSER_AUTHDB = os.environ["MONGO_DASHBOARDUSER_AUTH_DB"]

APPUSER_URI = f"mongodb://{APPUSER_USER}:{APPUSER_PASSWORD}@{HOST}:{PORT}/{APPUSER_AUTHDB}?authSource={APPUSER_AUTHDB}"
DASHBOARDUSER_URI = f"mongodb://{DASHBOARDUSER_USER}:{DASHBOARDUSER_PASSWORD}@{HOST}:{PORT}/{DASHBOARDUSER_AUTHDB}?authSource={DASHBOARDUSER_AUTHDB}"

