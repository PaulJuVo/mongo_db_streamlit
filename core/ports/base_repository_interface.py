from abc import ABC, abstractmethod

class BaseRepositoryInterface(ABC):
    
    @abstractmethod
    def insert_one(self, data):
        pass
    @abstractmethod
    def insert_many(self, data):
        pass
    @abstractmethod
    def get_collection_name(self) -> str:
        pass
    @abstractmethod
    def delete(self, filter):
        pass
    @abstractmethod
    def drop(self):
        pass
    @abstractmethod
    def create_time_series(self, config):
        pass
    @abstractmethod
    def execute_pipeline(self, pipeline):
        pass
    @abstractmethod
    def write_rejected_data(self, data):
        pass