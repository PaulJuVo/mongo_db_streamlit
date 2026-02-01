from abc import ABC, abstractmethod

class BaseRepositoryInterface(ABC):
    
    @abstractmethod
    def find_all(self):
        pass
    @abstractmethod
    def save(self):
        pass
    @abstractmethod
    def execute(self):
        pass