import csv

from HT.locust.src.core import config
from HT.locust.src.models.models import City, Forecast
from HT.locust.src.repository.abstaract_repo import AbstractDatabase
from HT.locust.src.repository.postgres import PostgresRepo


class DatabaseService:
    def __init__(self, db_repo: AbstractDatabase):
        self.db_repo = db_repo
        self.city_ids = ""
        self.forecast_ids = ""

    def write_test_data(self, cities: list[City], forecast: Forecast) -> type[
        list, list]:
        city_data = [city.create_tuple() for city in cities]
        ids = self.db_repo.write(city_data, cities[0].create_schema())
        ids = [str(city_id[0]) for city_id in ids]
        self.city_ids += ',' + ','.join(ids)

        forecast_data = [
            (id, 0, 30, "Sunny day") for id in ids
        ]

        ids = self.db_repo.write(forecast_data, forecast.create_schema())
        ids = [str(forecast_id[0]) for forecast_id in ids]
        self.forecast_ids += ',' + ','.join(ids)

    def init_from_file(self):
        file = 'cities.csv'
        create_temp_table_sql = """
                      CREATE TEMPORARY TABLE temp_cities ( 
                          id SERIAL,
                          name character varying(255)
                      )
                  """
        copy_sql = """
                     COPY temp_cities (name) FROM stdin WITH CSV HEADER
                     DELIMITER as ','
                  """
        move_data_sql = """
                      INSERT INTO public.cities (name)
                      SELECT name
                      FROM temp_cities
                      RETURNING id;
                  """

        ids = self.db_repo.init_from_file(
            create_temp_table_sql, copy_sql, move_data_sql, file
        )

        ids = [str(city_id[0]) for city_id in ids]
        self.city_ids += ',' + ','.join(ids)

        with open('forecasts.csv', 'w', encoding='UTF8') as f:
            for id in ids:
                writer = csv.writer(f)
                data = (id, 0, 30, 'sunny day')
                writer.writerow(data)
        file = 'forecasts.csv'
        create_temp_table_sql = """
                      CREATE TEMPORARY TABLE temp_forecast ( 
                          id SERIAL,
                          "cityId" bigint,
                          "dateTime" bigint,
                          temperature integer,
                          summary text
                      )
                  """

        copy_sql = """
                     COPY temp_forecast ("cityId","dateTime",temperature,summary) FROM stdin WITH CSV HEADER
                     DELIMITER as ','
                  """

        move_data_sql = """
                        INSERT INTO public.forecast ("cityId","dateTime",temperature,summary)
                        SELECT "cityId","dateTime",temperature,summary
                        FROM temp_forecast
                        RETURNING id;
                    """

        ids = self.db_repo.init_from_file(
            create_temp_table_sql, copy_sql, move_data_sql, file
        )
        ids = [str(forecast_id[0]) for forecast_id in ids]
        self.forecast_ids += ',' + ','.join(ids)

    def delete_test_data(self):
        self.db_repo.delete(
            self.city_ids[1:], 'public.cities'
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

    postgres_repo = PostgresRepo(config.DSN)
    postgres_service = DatabaseService(postgres_repo)
    postgres_service.write_test_data(city_data, Forecast())
    print(postgres_service.city_ids)
    print(postgres_service.forecast_ids)
    postgres_service.init_from_file()
    print(postgres_service.city_ids)
    print(postgres_service.forecast_ids)
    postgres_service.delete_test_data()
