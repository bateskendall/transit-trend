from typing import List, Any, Optional
import psycopg2
import requests
import gtfs_realtime_pb2
import logging
import os

logging.basicConfig(level=logging.INFO)

def fetch_binary_data(api_endpoint: str, api_key: str) -> Optional[bytes]:
    """
    Fetch binary data from the specified API endpoint using the provided API key.
    
    :param api_endpoint: The URL of the API endpoint to fetch data from.
    :param api_key: The API key to use for authentication.
    :return: The binary data fetched from the API, or None if an error occurs.
    """
    
    try:
        headers = {'x-api-key': api_key}
        response = requests.get(api_endpoint, headers=headers)
        response.raise_for_status()  # check for HTTP request errors
        return response.content
    except requests.RequestException as e:
        logging.exception(f"An error occurred while making a request:")
        return None

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

# DB parameters
db_params = {
    "dbname": os.getenv("DB_NAME", "default_db_name"),
    "user": os.getenv("DB_USER", "default_user"),
    "password": os.getenv("DB_PASSWORD", "default_db_password"),
    "host": os.getenv("DB_HOST", "default_db_host"),
    "port": os.getenv("DB_PORT", "default_db_port"),
}

def main():
    # DB connection
    conn = psycopg2.connect(**db_params)

    try:
        # API details
        api_key = os.getenv('API_KEY', "default_api_key")
        api_endpoint_urls = ["https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace",  # ACE Lines API Endpoint
                             "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm", # BDFM Lines API Endpoint
                             "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g",    # G Line API Endpoint
                             "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz",   # JZ Lines API Endpoint
                             "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw", # NQRW Lines API Endpoint
                             "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l",    # L Line API Endpoint
                             "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs",      # 1-7 Lines API Endpoint
                             "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-si"]   # SIR API Endpoint
        
        ensure_table_exists(conn)
        
        # Fetch binary data
        binary_data_list = []
        
        # Loop through endpoint urls to fetch from each endpoint
        for url in api_endpoint_urls:
            binary_data = fetch_binary_data(url, api_key)
            if binary_data:
                binary_data_list.append(binary_data)
        
        # Store binary data
        if binary_data_list:
            store_binary_data(binary_data_list, conn)
    finally:
        # Close DB connection
        conn.close()

if __name__ == "__main__":
    main()
