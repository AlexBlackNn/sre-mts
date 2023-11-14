from HT.locust.src.core import config
from HT.locust.src.database.db import PostgresConnectoion


class PostgresRepo:
    def __init__(self, dsn):
        self.dsn = dsn

    @staticmethod
    def create_param_template(number):
        return '(' + ('%s,' * number)[:-1] + ")"

    def get_one_item(self, id):
        pass

    def write_one_item(self, id):
        pass

    def write_several_items(self, data, schema):
        with PostgresConnectoion(
                self.dsn
        ) as postgresql_connection, postgresql_connection.cursor() as cursor:
            number_params = self.create_param_template(len(data[0]))
            args = ','.join(
                cursor.mogrify(number_params, item).decode() for item in data
            )
            cursor.execute(f"""INSERT INTO {schema} VALUES {args}; """)


if __name__ == '__main__':
    postgres_repo = PostgresRepo(config.DSN)

    data = [
        ('TestCity1',),
        ('TestCity2',)
    ]
    schema = 'cities (name)'
    postgres_repo.write_several_items(data, schema)
    data = [
        (1, 0, 30, "Sunny day"),
        (2, 0, 25, "Wet day"),
    ]
    schema = 'forecast ("cityId","dateTime",temperature,summary)'
    postgres_repo.write_several_items(data, schema)

    with PostgresConnectoion(config.DSN) as postgresql_connection:
        cursor = postgresql_connection.cursor()
        sql = '''SELECT * FROM cities'''
        cursor.execute(sql)
        postgresql_connection.commit()
        publisher_records = cursor.fetchall()
        print(publisher_records)
