from core.ports.incomeStatement_repo_interface import IncomeStatement_Repository_interface

class IncomeStatement_Repository(IncomeStatement_Repository_interface):
    def __init__(self, db, session):
        self.db = db
        self.session = session
        self.collection = "incomeStatement"

    def execute(self, query : str):
        
        coll = self.db.get_collection(self.collection)
        print(coll.full_name)
        
        return None

    def find_all(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError