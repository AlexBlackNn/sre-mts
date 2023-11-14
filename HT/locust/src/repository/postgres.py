from HT.locust.src.core import config
from HT.locust.src.database.db import PostgresConnectoion
from HT.locust.src.repository.abstaract_repo import AbstractDatabase

import io

class PostgresRepo(AbstractDatabase):
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

    def init_from_file(self):
        with PostgresConnectoion(
                self.dsn
        ) as postgresql_connection, postgresql_connection.cursor() as cursor:
            data = io.StringIO()
            data.write('1111, Михаил Михайлови1ч')
            data.seek(0)
            cursor.copy_expert(
                """COPY public.cities FROM STDIN (FORMAT 'csv', HEADER false)""",
                data
            )


if __name__ == '__main__':

    postgres_repo = PostgresRepo(config.DSN)
    postgres_repo.init_from_file()