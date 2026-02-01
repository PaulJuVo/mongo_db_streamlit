from core.ports.financeData_repo_interface import FinanceData_Repository_interface

class FinanceData_Repository(FinanceData_Repository_interface):
    def __init__(self, db, session):
        self.db = db
        self.session = session
        self.collection = "financeData"

    def execute(self, query : str):
        
        coll = self.db.get_collection(self.collection)
        print(coll.full_name)
        
        return None

    def find_all(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError