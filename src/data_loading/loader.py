import psycopg2
import logging
from typing import List

def store_binary_data(binary_data_list: List[bytes], conn: psycopg2.extensions.connection) -> None:
    """
    Load binary data into the database for later use.
    
    Args:
        binary_data_list (List[bytes]): A list containing all binary files fetched from the API endpoints.
        conn (psycopg2.extensions.connection): A database connection object.
    """
    
    for i, binary_data in enumerate(binary_data_list):
        try:
            with conn.cursor() as cur:
                query = "INSERT INTO Realtime_Binary_Data (binary_data) VALUES (%s::bytea);"
                cur.execute(query, (binary_data,))
            conn.commit()
            logging.info(f"Stored binary data entry")
        except psycopg2.Error as e:
            logging.exception(f"A database error occurred with binary data entry {i}")
            conn.rollback()
            
def ensure_table_exists(conn: psycopg2.extensions.connection) -> None:
    """
    Create tables for storing extracted data if they don't already exist.

    Args:
        conn (psycopg2.extensions.connection): A database connection object.
    """
    
    commands = (
        """
        CREATE TABLE IF NOT EXISTS realtime_trip_updates (
            id SERIAL PRIMARY KEY,
            trip_id VARCHAR(255) NOT NULL,
            route_id VARCHAR(255),
            start_date DATE,
            schedule_relationship INTEGER,
            arrival_time TIME,
            departure_time TIME,
            stop_id VARCHAR(255),
            last_updated TIMESTAMP DEFAULT NOW()
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS realtime_vehicle_positions (
            id SERIAL PRIMARY KEY,
            trip_id VARCHAR(255),
            route_id VARCHAR(255),
            current_stop_sequence INTEGER,
            stop_id VARCHAR(255),
            current_status INTEGER,
            timestamp TIMESTAMP,
            last_updated TIMESTAMP DEFAULT NOW()
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS realtime_alerts (
            id SERIAL PRIMARY KEY,
            alert_id VARCHAR(255),
            trip_id VARCHAR(255),
            route_id VARCHAR(255),
            description_text TEXT,
            last_updated TIMESTAMP DEFAULT NOW()
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS realtime_binary_data (
            id SERIAL PRIMARY KEY,
            binary_data BYTEA,
            timestamp TIMESTAMP DEFAULT NOW()
        )
        """
    )
    try:
        with conn.cursor() as cur:
            # create table one by one
            for command in commands:
                cur.execute(command)
            cur.close()
            # commit the changes
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        logging.exception("An error occurred while creating tables: %s", error)
        # in case of error, rollback the transaction
        conn.rollback()