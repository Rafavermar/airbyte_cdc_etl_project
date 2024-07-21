import psycopg2

try:
    conn = psycopg2.connect(
        dbname="airbyte",
        user="airbyte",
        password="airbyte",
        host="localhost",
        port="5432"
    )
    print("Conexión exitosa")
    conn.close()
except Exception as e:
    print("No se pudo conectar:", e)
