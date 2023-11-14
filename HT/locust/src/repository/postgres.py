from HT.locust.src.core import config
from HT.locust.src.database.db import PostgresConnectoion
from HT.locust.src.repository.abstaract_repo import AbstractDatabase


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
