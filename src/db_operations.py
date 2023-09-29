import psycopg2
import logging
from typing import List, Any

def store_binary_data(binary_data_list: List[bytes], conn: psycopg2.extensions.connection) -> None:
    """
    Load binary data into database for later use.
    
    :param binary_data_list: A list containing all binary files fetched from the API endpoints.
    :param conn: The database connection.
    """
    
    for i, binary_data in enumerate(binary_data_list):
        try:
            with conn.cursor() as cur:
                query = "INSERT INTO Realtime_Binary_Data (binary_data) VALUES (%s);"
                cur.execute(query, (binary_data,))
            conn.commit()
            logging.info(f"Stored binary data entry {i}")
        except psycopg2.Error as e:
            logging.exception(f"A database error occurred with binary data entry {i}")
            conn.rollback()
            
def ensure_table_exists(conn: psycopg2.extensions.connection) -> None:
    """
    Create the table for storing binary data if it doesn't already exist.

    :param conn: The database connection.
    """

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Realtime_Binary_Data (
                id SERIAL PRIMARY KEY,
                binary_data BYTEA,
                timestamp TIMESTAMP DEFAULT NOW()
            );
        """)
        conn.commit()