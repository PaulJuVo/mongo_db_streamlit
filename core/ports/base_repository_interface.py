from abc import ABC, abstractmethod
from core.ports.cursor import Cursor
from typing import Any, Optional

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
    def find(self, filter : Optional[dict] = None, batch_size : Optional[int] = None, limit : Optional[int] = None, projection : Optional[dict] = None, sort : Optional[dict] = None) -> Cursor:
        pass
    @abstractmethod
    def find_distinct(self,key, filter = None) -> list:
        pass
    @abstractmethod
    def find_one(self, filter : Optional[dict] = None) -> Any:
        pass
    @abstractmethod
    def create_index(self, keys : list[tuple], unique : bool):
        pass