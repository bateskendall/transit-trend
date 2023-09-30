import psycopg2
from config import db_params, api_key, api_endpoint_urls
from src.data_extraction import fetch_binary_data
from src.data_loading import store_binary_data, ensure_table_exists

if __name__ == "__main__":
    # DB connection
    conn = psycopg2.connect(**db_params)

    try:
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