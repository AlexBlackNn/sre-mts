import psycopg2


class PostgresConnectoion:
    """Context manager for postgres."""

    def __init__(self, dsn: dict):
        self.connection = psycopg2.connect(**dsn)

    def __enter__(self):
        return self.connection

    def __exit__(self, error: Exception, value: object, traceback: object):
        self.connection.commit()
        self.connection.close()
