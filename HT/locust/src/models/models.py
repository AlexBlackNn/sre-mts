from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass()
class Table(ABC):
    id: int = field(default='None')
    postgres_name_table: str = field(default='None')
    init_file: str = field(default='None')

    @staticmethod
    def _show(key):
        # some fields should not be put in sql expression
        return (
                key != 'postgres_name_table' and
                key != 'id' and
                key != 'init_file'
        )

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
                key != 'id' and
                key != 'postgres_name_table' and
                key != 'init_file') ]
        )

    def create_schema(self) -> str:
        return self.postgres_name_table + ' ' + self.create_template()

    @abstractmethod
    def create_temp_table_sql(self) -> str:
        pass

    @abstractmethod
    def create_copy_sql(self) -> str:
        pass

    @abstractmethod
    def create_move_data_sql(self) -> str:
        pass


@dataclass()
class City(Table):
    name: str = field(default='None')
    postgres_name_table: str = field(default='cities')

    @staticmethod
    def create_temp_table_sql() -> str:
        return """
                CREATE TEMPORARY TABLE temp_cities ( 
                id SERIAL,
                name character varying(255)
                )
                """

    @staticmethod
    def create_copy_sql() -> str:
        return """
                COPY temp_cities (name) FROM stdin WITH CSV HEADER
                DELIMITER as ',' 
                """

    @staticmethod
    def create_move_data_sql() -> str:
        return """
               INSERT INTO public.cities (name)
               SELECT name
               FROM temp_cities
               RETURNING id;
               """

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

    @staticmethod
    def create_temp_table_sql() -> str:
        return """
                  CREATE TEMPORARY TABLE temp_forecast ( 
                  id SERIAL,
                  "cityId" bigint,
                  "dateTime" bigint,
                  temperature integer,
                  summary text
                  )
                  """

    @staticmethod
    def create_copy_sql() -> str:
        return """
               COPY temp_forecast ("cityId","dateTime",temperature,summary)
               FROM stdin WITH CSV HEADER
               DELIMITER as ','
               """

    @staticmethod
    def create_move_data_sql() -> str:
        return """
            INSERT INTO public.forecast (
            "cityId","dateTime",temperature,summary
            )
            SELECT "cityId","dateTime",temperature,summary
            FROM temp_forecast
            RETURNING id;
            """


if __name__ == '__main__':
    city = City(name='Moscow')
    print(city.create_schema())
    print(city.create_tuple())
    forecast = Forecast()
    print(forecast.create_schema())
