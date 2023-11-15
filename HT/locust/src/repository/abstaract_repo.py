from abc import ABC, abstractmethod


class AbstractDatabase(ABC):
    @abstractmethod
    def write(self, data: list[str], schema: str) -> list[tuple[int,]]:
        pass

    @abstractmethod
    def init_from_file(self):
        pass
