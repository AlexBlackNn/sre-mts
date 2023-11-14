from HT.locust.src.core import config
from HT.locust.src.database.db import PostgresConnectoion


class PostgresRepo:
    def __init__(self, dsn):
        self.dsn = dsn

    @staticmethod
    def __create_param_template(number):
        return '(' + ('%s,' * number)[:-1] + ")"

    def write(self, data, schema):
        with PostgresConnectoion(
                self.dsn
        ) as postgresql_connection, postgresql_connection.cursor() as cursor:
            number_params = self.__create_param_template(len(data[0]))
            args = ','.join(
                cursor.mogrify(number_params, item).decode() for item in data
            )
            cursor.execute(
                f"""INSERT INTO {schema} VALUES {args} RETURNING id; """
            )
            return cursor.fetchall()


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


    def write_test_data(city_data: list[tuple]) -> type[list, list]:
        postgres_repo = PostgresRepo(config.DSN)

        schema = 'cities (name)'
        city_ids = postgres_repo.write(city_data, schema)

        forecast_data = [
            (city_id[0], 0, 30, "Sunny day") for city_id in city_ids
        ]

        schema = 'forecast ("cityId","dateTime",temperature,summary)'
        forecast_ids = postgres_repo.write(forecast_data, schema)
        return city_ids, forecast_ids

    print(write_test_data(city_data))
