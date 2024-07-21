import psycopg2
from psycopg2 import sql
from src.config.settings import DATABASE


class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = psycopg2.connect(**DATABASE)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()


def initialize_database():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS employees (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        position VARCHAR(100),
        salary NUMERIC
    );
    '''

    set_replica_identity_query = '''
    ALTER TABLE employees REPLICA IDENTITY FULL;
    '''

    create_publication_query = '''
    CREATE PUBLICATION my_publication FOR TABLE employees;
    '''

    create_replication_slot_query = '''
    SELECT * FROM pg_create_logical_replication_slot('airbyte_slot', 'pgoutput');
    '''

    with DatabaseConnection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
            connection.commit()
            cursor.execute(set_replica_identity_query)
            connection.commit()
            cursor.execute(create_publication_query)
            connection.commit()
            cursor.execute(create_replication_slot_query)
            connection.commit()
