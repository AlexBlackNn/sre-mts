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
            cursor.execute(f"""INSERT INTO {schema} VALUES {args} RETURNING id; """)
            return cursor.fetchall()


if __name__ == '__main__':
    postgres_repo = PostgresRepo(config.DSN)

    data = [
        ('TestCity1',),
        ('TestCity2',),
        ('TestCity3', ),
        ('TestCity4', ),
        ('TestCity5', ),
        ('TestCity6', ),
        ('TestCity7', ),
        ('TestCity8', )
    ]
    schema = 'cities (name)'
    ids = postgres_repo.write(data, schema)
    print(ids)
    data = [
        (1, 0, 30, "Sunny day"),
        (2, 0, 25, "Wet day"),
        (3, 0, 30, "Sunny day"),
        (4, 0, 25, "Wet day"),
    ]
    schema = 'forecast ("cityId","dateTime",temperature,summary)'
    ids = postgres_repo.write(data, schema)
    print(ids)
    with PostgresConnectoion(config.DSN) as postgresql_connection:
        cursor = postgresql_connection.cursor()
        sql = '''SELECT * FROM cities'''
        cursor.execute(sql)
        postgresql_connection.commit()
        publisher_records = cursor.fetchall()
        print(publisher_records)
