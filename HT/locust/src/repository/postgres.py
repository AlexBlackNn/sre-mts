import csv

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

    def init_from_file(self, create_temp_table_sql, copy_sql, move_data_sql,
                       file):
        """
        Copying data from a temporary table to the target table in PostgreSQL
        is generally a fast operation, especially when dealing with large
        datasets. PostgreSQL is designed to handle bulk data operations
        efficiently.

        The performance of the data copy operation can be influenced by
        several factors:

        1. Hardware and server resources: The speed of the disk where the
         database files are stored, the amount of available memory, and the
         processing power of the server can impact the speed of the data copy
         operation.

        2. Indexes and constraints: If the target table (public.cities) has
        indexes or constraints, the data copy operation may take longer as the
         database needs to validate and update these structures during the
         insertion.

        3. Concurrent operations: If multiple operations are occurring
        concurrently, such as other write operations on the target table or
        heavy read operations on the server, it may affect the performance of
         the data copy operation.

        Considering these factors, if you are dealing with a large amount of
        data, it might be worthwhile to use the COPY FROM operation followed
        by the INSERT INTO ... SELECT statement to return auto-generated IDs.
        This approach minimizes the overhead of individual insertions and can
         generally provide better performance than inserting records one by one.

        However, it's always recommended to test and benchmark different
        approaches with your specific dataset and workload to determine the
        best solution for your use case. Monitoring performance and optimizing
        the database configuration can also help ensure efficient data copying.
        """
        with PostgresConnectoion(
                self.dsn
        ) as postgresql_connection, postgresql_connection.cursor() as cursor:
            cursor.execute(create_temp_table_sql)

            with open(file, 'r') as f:
                cursor.copy_expert(sql=copy_sql, file=f)

            cursor.execute(move_data_sql)
            return cursor.fetchall()


if __name__ == '__main__':

    def init_from_file():
        postgres_repo = PostgresRepo(config.DSN)
        file = '../../../../cities.csv'
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

        cities_id = postgres_repo.init_from_file(
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

        forecast_id = postgres_repo.init_from_file(
            create_temp_table_sql, copy_sql, move_data_sql, file
        )
        return cities_id, forecast_id


    print(init_from_file())
