from HT.locust.src.core import config
from HT.locust.src.database.db import PostgresConnectoion

class PostgresRepo:
    def __init__(self, dsn):
        self.dsn = dsn

    def get_one_item(self, id):
        pass

    def write_one_item(self, id):
        pass

    def write_several_items(self):
        with PostgresConnectoion(self.dsn) as postgresql_connection, postgresql_connection.cursor() as cursor:
            data = [
                ('TestCity1',),
                ('TestCity2',)
            ]
            args = ','.join(cursor.mogrify("(%s)", item).decode() for item in data)
            cursor.execute(
                f"""
                INSERT INTO cities (name)
                VALUES {args};
                """
            )


if __name__ == '__main__':
    postgres_repo = PostgresRepo(config.DSN)
    postgres_repo.write_several_items()

    with PostgresConnectoion(config.DSN) as postgresql_connection:
        cursor = postgresql_connection.cursor()
        sql = '''SELECT * FROM cities'''
        cursor.execute(sql)
        postgresql_connection.commit()
        publisher_records = cursor.fetchall()
        print(publisher_records)
