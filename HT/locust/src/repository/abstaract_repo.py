from abc import ABC, abstractmethod


class AbstractDatabase(ABC):
    @abstractmethod
    def write(self, data: list[str], schema: str) -> list[tuple[int,]]:
        pass
