import psycopg2

from HT.locust.src.database.postgres import PostgresConnectoion
from HT.locust.src.models.models import Table
from HT.locust.src.repository.abstaract_repo import AbstractDatabase


class PostgresRepo(AbstractDatabase):
    def __init__(self, dsn):
        self.dsn = dsn
        self.postgres_connection = psycopg2.connect(**dsn)
        self.cursor = self.postgres_connection.cursor()

    @staticmethod
    def __create_param_template(number):
        return '(' + ('%s,' * number)[:-1] + ")"

    def write(self, models: list) -> list[str]:

            data = [model.create_tuple() for model in models]
            number_params = self.__create_param_template(len(data[0]))
            args = ','.join(
                self.cursor.mogrify(number_params, item).decode() for item in data
            )
            self.cursor.execute(
                f"""
                INSERT INTO {models[0].create_schema()} VALUES
                {args} RETURNING id; 
                 """
            )
            return [str(city_id[0]) for city_id in self.cursor.fetchall()]

    def init_from_file(self, model: Table):
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
            cursor.execute(model.create_temp_table_sql())

            with open(model.init_file, 'r') as f:
                cursor.copy_expert(sql=model.create_copy_sql(), file=f)

            cursor.execute(model.create_move_data_sql())
            return [str(city_id[0]) for city_id in cursor.fetchall()]

    def delete(self, data, schema):
        with PostgresConnectoion(
                self.dsn
        ) as postgresql_connection, postgresql_connection.cursor() as cursor:
            data = ",".join(data)
            cursor.execute(f"""DELETE FROM {schema} WHERE id IN ({data});""")
