import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

DATABASE = {
    'dbname': os.getenv('DB_NAME', 'airbyte'),
    'user': os.getenv('DB_USER', 'airbyte'),
    'password': os.getenv('DB_PASSWORD', 'airbyte'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', 5432),
}
