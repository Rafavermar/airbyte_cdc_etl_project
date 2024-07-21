import sys
import os
import psycopg2
from psycopg2 import sql
from psycopg2.errors import DuplicateObject
from src.config.settings import DATABASE
from dotenv import load_dotenv

# Asegurar que el directorio src está en sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def initialize_database():
    print("Database configuration:", DATABASE)

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
    check_publication_exists_query = '''
    SELECT 1 FROM pg_publication WHERE pubname = 'my_publication';
    '''

    try:
        print("Trying to connect to the database with the following settings:")
        print("Host:", DATABASE['host'])
        print("Port:", DATABASE['port'])
        print("User:", DATABASE['user'])
        print("Database name:", DATABASE['dbname'])
        with psycopg2.connect(**DATABASE) as connection:
            with connection.cursor() as cursor:
                print("Creating table if not exists...", file=open('initialize_log.txt', 'a'))
                cursor.execute(create_table_query)
                connection.commit()
                print("Setting replica identity to FULL...", file=open('initialize_log.txt', 'a'))
                cursor.execute(set_replica_identity_query)
                connection.commit()

                print("Checking if publication exists...", file=open('initialize_log.txt', 'a'))
                cursor.execute(check_publication_exists_query)
                publication_exists = cursor.fetchone()

                if not publication_exists:
                    print("Creating publication...", file=open('initialize_log.txt', 'a'))
                    cursor.execute(create_publication_query)
                    connection.commit()
                else:
                    print("Publication already exists.", file=open('initialize_log.txt', 'a'))

                print("Creating replication slot if not exists...", file=open('initialize_log.txt', 'a'))
                try:
                    cursor.execute(create_replication_slot_query)
                    connection.commit()
                except (DuplicateObject, psycopg2.errors.UniqueViolation):
                    print("Replication slot 'airbyte_slot' already exists", file=open('initialize_log.txt', 'a'))
    except psycopg2.OperationalError as e:
        print("OperationalError connecting to the database:", e)
    except Exception as e:
        print("Error connecting to the database:", e)

if __name__ == "__main__":
    initialize_database()
    print("Initialization complete.", file=open('initialize_log.txt', 'a'))
