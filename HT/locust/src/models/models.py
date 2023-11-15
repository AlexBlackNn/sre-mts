import datetime
import uuid
from abc import ABC
from dataclasses import dataclass, field


@dataclass()
class Table(ABC):
    id: int = field(default='None')
    postgres_name_table: str = field(default='None')

    @staticmethod
    def _show(key):
        # some fields should not be put in sql expression
        return (key != 'postgres_name_table' and key != 'id')

    def create_template(self) -> str:
        """Create template for postgres sql load expression."""
        names = tuple(
            [key for key, value in self.__dict__.items() if self._show(key)]
        )
        columns = ','.join(names)
        return '(' + columns + ')'

    def create_tuple(self):
        """Create data for postgres sql load expression."""
        return tuple([value for key, value in self.__dict__.items() if (
                key != 'postgres_name_table') and key != 'id'])

    def create_schema(self) -> str:
        return self.postgres_name_table + ' ' + self.create_template()


@dataclass()
class City(Table):
    name: str = field(default='None')
    postgres_name_table: str = field(default='cities')


@dataclass()
class Forecast(Table):
    city_id: int = field(default=1)
    date_time: int = field(default=0)
    temperature: int = field(default=0)
    summary: str = field(default='None')
    postgres_name_table: str = field(default='forecast')

    def create_schema(self) -> str:
        schema = super().create_schema()
        return schema.replace(
            "date_time", "\"dateTime\""
        ).replace("city_id", "\"cityId\"")


if __name__ == '__main__':
    city = City(name='Moscow')
    print(city.create_schema())
    print(city.create_tuple())
    forecast = Forecast()
    print(forecast.create_schema())
