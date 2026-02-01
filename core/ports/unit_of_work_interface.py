from abc import ABC, abstractmethod
from core.ports.companyData_repo_interface import CompanyData_Repository_interface
from core.ports.eodPrice_repo_interface import EodPrice_Repository_interface
from core.ports.financeData_repo_interface import FinanceData_Repository_interface
from core.ports.incomeStatement_repo_interface import IncomeStatement_Repository_interface
from core.ports.profile_repo_interface import Profile_Repository_interface


class unit_of_work_interface(ABC):
    eodPrice: EodPrice_Repository_interface
    incomeStatement:IncomeStatement_Repository_interface
    profile:Profile_Repository_interface
    financeData:FinanceData_Repository_interface
    companyData:CompanyData_Repository_interface

    @abstractmethod
    def __init__(self, client):
        pass
    @abstractmethod
    def __enter__(self): 
        return self
    @abstractmethod
    def commit(self):
        pass
    @abstractmethod
    def rollback(self):
        pass
    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
