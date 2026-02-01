from core.ports.companyData_repo_interface import CompanyData_Repository_interface


class CompanyData_Repository(CompanyData_Repository_interface):
    def __init__(self, db, session):
        self.db = db
        self.session = session
        self.collection = "companyData"

    def execute(self, query : str):
        
        coll = self.db.get_collection(self.collection)
        print(coll.full_name)
        
        return None

    def find_all(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError