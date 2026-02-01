from core.ports.eodPrice_repo_interface import EodPrice_Repository_interface
from pymongo.database import Database

class EodPrice_Repository(EodPrice_Repository_interface):
    def __init__(self, db : Database, session):
        self.db = db
        self.session = session
        # TODO mit config verbinden
        self.collection_name = "eodPrice"

    def execute(self, query : str):
        print("Sucsessful")
        coll = self.db.get_collection(self.collection_name)
        coll.insert_one({"test":2})
        print(coll.full_name)
        #print(self.db.command(query))
        return None

    def find_all(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError