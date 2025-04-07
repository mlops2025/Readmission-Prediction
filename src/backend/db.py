import psycopg2
from psycopg2.extras import execute_values
import os
from psycopg2 import sql

# You can move these to a .env later
DB_CONFIG = {
    "dbname": "mlopsneu2025",
    "user": "postgres",
    "password": "mlops2025",
    "host": "34.123.77.199",
    "port": 5432,
}

def insert_prediction(data_dict):
    try:
        # Open DB connection
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                # Format column names and placeholders safely
                columns = list(data_dict.keys())
                values = list(data_dict.values())

                insert_query = sql.SQL("""
                    INSERT INTO patients_data ({fields})
                    VALUES ({placeholders})
                """).format(
                    fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
                    placeholders=sql.SQL(', ').join(sql.Placeholder() * len(columns))
                )

                cursor.execute(insert_query, values)
                conn.commit()
                print("✅ Prediction inserted into database.")

    except Exception as e:
        print(f"[DB ERROR] {e}")