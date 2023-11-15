import csv

from HT.locust.src.core import config
from HT.locust.src.repository.abstaract_repo import AbstractDatabase
from HT.locust.src.repository.postgres import PostgresRepo


class DatabaseService:
    def __init__(self, db_repo: AbstractDatabase):
        self.db_repo = db_repo

    def write_test_data(self, city_data: list[tuple]) -> type[list, list]:
        schema = 'cities (name)'
        city_ids = self.db_repo.write(city_data, schema)

        forecast_data = [
            (city_id[0], 0, 30, "Sunny day") for city_id in city_ids
        ]

        schema = 'forecast ("cityId","dateTime",temperature,summary)'
        forecast_ids = self.db_repo.write(forecast_data, schema)
        return city_ids, forecast_ids

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

        cities_id = self.db_repo.init_from_file(
            create_temp_table_sql, copy_sql, move_data_sql, file
        )
        with open('forecasts.csv', 'w', encoding='UTF8') as f:
            for city_id in cities_id:
                writer = csv.writer(f)
                data = (city_id[0], 0, 30, 'sunny day')
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

        forecast_id = self.db_repo.init_from_file(
            create_temp_table_sql, copy_sql, move_data_sql, file
        )
        return cities_id, forecast_id


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
    postgres_service = DatabaseService(postgres_repo)
    print(postgres_service.write_test_data(city_data))
    print(postgres_service.init_from_file())
