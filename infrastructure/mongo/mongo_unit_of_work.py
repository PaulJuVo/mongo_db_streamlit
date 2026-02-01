from core.ports.unit_of_work_interface import unit_of_work_interface 
from infrastructure.mongo.mongo_connection import Mongo_Connection 
from infrastructure.mongo.mongo_user import Mongo_user
from infrastructure.mongo.repositories import * 
from config.mongo_config import REPO_MAP
from typing import Optional

# FÜR MULTI_FILE ACID TRANSAKTIONEN und für Bündelung der verschiedenen Repositories
class MongoUnitOfWork(unit_of_work_interface):

    def __init__(self, connection : Mongo_Connection, db_user : Mongo_user):
        self.connection = connection
        self.user = db_user
        self.db = connection.get_db()

        self.eodPrice: Optional[EodPrice_Repository] = None
        self.financeData: Optional[FinanceData_Repository] = None
        self.companyData: Optional[CompanyData_Repository] = None
        self.profile: Optional[Profile_Repository] = None
        self.incomeStatement: Optional[IncomeStatement_Repository] = None
          

    def __enter__(self):
        self.session = self.connection.client.start_session()
        self.session.start_transaction()
        self._build_repositories()
        return self

    def commit(self):
        self.session.commit_transaction()

    def rollback(self):
        self.session.abort_transaction()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO
        if exc_type:
            self.rollback()
        else:
            self.commit()

        self.session.end_session()
    
    def _build_repositories(self):
        for name, repo_cls in REPO_MAP[self.user]:
            # gleiche wie self.name = repo_cls...
            # TODO hier wird ein repo erstellt mit der auth db des USers! Das ist shit repo sollte 
            setattr(self, name, repo_cls(self.db, self.session))

