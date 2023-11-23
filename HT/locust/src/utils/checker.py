from abc import ABC, abstractmethod
from typing import Any


class Checker(ABC):
    @abstractmethod
    def check(self, response):
        pass


class CheckerPipline:
    def __init__(self):
        self.__checker_pipline: list[Checker] = []

    def add(self, checker: Checker):
        if isinstance(checker, Checker):
            self.__checker_pipline.append(checker)
        else:
            raise TypeError('Wrong Type of item')

    def execute(self, response):
        for checker in self.__checker_pipline:
            checker.check(response)


class CheckResponseStatus(Checker):
    def __init__(self, response_code: int):
        self.response_code = response_code

    def check(self, response):
        if response.status_code != self.response_code:
            response.failure(f'failed with status code {response.status_code}')


class CheckResponseValue(Checker):
    def __init__(self, expected_value: Any, field='name'):
        self.expected_value = expected_value
        self.field = field

    def check(self, response):
        if response.json()[0][self.field] != self.expected_value:
            response.failure(
                f"failed with unexpected value in 'name' ->"
                f" {response.json()[0][self.field]}"
            )


class CheckResponseElapsedTotalSeconds(Checker):
    def __init__(self, elapsed_total_sec: int):
        self.elapsed_total_sec = elapsed_total_sec

    def check(self, response):
        if response.elapsed.total_seconds() > self.elapsed_total_sec:
            response.failure(
                f"failed with too long request -> "
                f"{response.elapsed.total_seconds()}"
            )
