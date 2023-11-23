import csv

from HT.locust.src.core import config_new
from HT.locust.src.models.models import City, Forecast
from HT.locust.src.repository.abstaract_repo import AbstractDatabase
from HT.locust.src.repository.postgres import PostgresRepo


class DatabaseService:
    def __init__(self, db_repo: AbstractDatabase):
        self.db_repo = db_repo
        self.city_ids = []
        self.forecast_ids = []

    def add_city_id(self, _id: str):
        self.city_ids.append(_id)

    def add_forecast_id(self, _id: str):
        self.forecast_ids.append(_id)

    def write_test_data(self, cities: list[City]):
        ids = self.db_repo.write(cities)
        self.city_ids += ids
        forecasts = [
            Forecast(
                city_id=id,
                date_time=0,
                temperature=30,
                summary="Sunny day"
            ) for id in ids
        ]
        self.forecast_ids += self.db_repo.write(forecasts)

    def init_from_file(self):
        city = City(init_file='cities.csv')
        ids = self.db_repo.init_from_file(city)
        self.city_ids += ids

        with open('forecasts.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            for id in ids:
                data = (id, 0, 30, 'sunny day')
                writer.writerow(data)

        forecast = Forecast(init_file='forecasts.csv')
        ids = self.db_repo.init_from_file(forecast)
        self.forecast_ids += ids

    def delete_test_data(self):
        self.db_repo.delete(
            self.city_ids, 'public.cities'
        )
        # self.city_ids = ""
        # self.forecast_ids = ""


if __name__ == '__main__':
    city_data = [
        City(name='TestCity1'),
        City(name='TestCity2'),
        City(name='TestCity3'),
        City(name='TestCity4'),
        City(name='TestCity5'),
        City(name='TestCity6'),
    ]

    postgres_repo = PostgresRepo(config_new.DSN)
    postgres_service = DatabaseService(postgres_repo)
    postgres_service.write_test_data(city_data)
    print(postgres_service.city_ids)
    print(postgres_service.forecast_ids)
    postgres_service.init_from_file()
    print(postgres_service.city_ids)
    print(postgres_service.forecast_ids)
    postgres_service.delete_test_data()
