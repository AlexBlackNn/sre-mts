from HT.locust.src.core import config
from HT.locust.src.repository.abstaract_repo import AbstractDatabase
from HT.locust.src.repository.postgres import PostgresRepo


class PostgresService:
    def __init__(self, db_repo: AbstractDatabase):
        self.db_repo = db_repo

    def write_test_data(self, city_data: list[tuple]) -> type[list, list]:
        self.db_repo = PostgresRepo(config.DSN)

        schema = 'cities (name)'
        city_ids = self.db_repo.write(city_data, schema)

        forecast_data = [
            (city_id[0], 0, 30, "Sunny day") for city_id in city_ids
        ]

        schema = 'forecast ("cityId","dateTime",temperature,summary)'
        forecast_ids = self.db_repo.write(forecast_data, schema)
        return city_ids, forecast_ids


if __name__ == '__main__':
    city_data = [
        ('TestCity1',),
        ('TestCity2',),
        ('TestCity3',),
        ('TestCity4',),
        ('TestCity5',),
        ('TestCity6',),
        ('TestCity7',),
        ('TestCity8',)
    ]

    postgres_repo = PostgresRepo(config.DSN)
    postgres_service = PostgresService(postgres_repo)
    print(postgres_service.write_test_data(city_data))
