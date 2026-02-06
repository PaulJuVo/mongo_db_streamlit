from abc import ABC, abstractmethod

class BaseRepositoryInterface(ABC):
    
    @abstractmethod
    def find_all(self):
        pass
    @abstractmethod
    def insert_one(self, data):
        pass
    @abstractmethod
    def insert_many(self, data):
        pass
    @abstractmethod
    def save(self):
        pass
    @abstractmethod
    def exists(self, filter):
        pass
    @abstractmethod
    def execute(self):
        pass
    @abstractmethod
    def get_collection_name(self) -> str:
        pass
    @abstractmethod
    def delete(self, filter):
        pass