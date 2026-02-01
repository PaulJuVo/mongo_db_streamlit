from abc import ABC, abstractmethod
from typing import Any, List

class CompanyData_Repository_interface(ABC):

    @abstractmethod
    def execute(self, query: str) -> Any:
        pass

    @abstractmethod
    def find_all(self) -> List[Any]:
        pass

    @abstractmethod
    def save(self, data: Any) -> None:
        pass