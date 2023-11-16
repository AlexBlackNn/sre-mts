from abc import ABC, abstractmethod

from HT.locust.src.models.models import Table


class AbstractDatabase(ABC):
    @abstractmethod
    def write(self, models: list[Table]) -> list[str]:
        pass

    @abstractmethod
    def init_from_file(self, model: Table) -> list[str]:
        pass
