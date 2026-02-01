from abc import ABC, abstractmethod

class db_repository_interface(ABC):
    
    @abstractmethod
    def find_all(self):
        pass
    @abstractmethod
    def save(self):
        pass
    @abstractmethod
    def execute(self, query : str, collection : str):
        pass