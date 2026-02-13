from abc import ABC, abstractmethod
from core.ports.cursor import Cursor
from typing import Optional

class BaseRepositoryInterface(ABC):
    
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
    @abstractmethod
    def find(self, filter : Optional[dict] = None, batch_size : Optional[int] = None, limit : Optional[int] = None) -> Cursor:
        pass
    @abstractmethod
    def create_index(self, keys : list[tuple], unique : bool):
        pass