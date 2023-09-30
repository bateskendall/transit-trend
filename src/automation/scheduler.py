import logging
import schedule
import time
from src.data_extraction.extractor import fetch_binary_data
from src.data_loading.loader import store_binary_data, ensure_table_exists
from config import api_key, api_endpoint_urls

def job(conn) -> None:
    logging.info("Starting job...")
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
    except Exception as e:
        logging.error(f"Error: {e}")

def setup_schedule(conn) -> None:
    """
    Schedules tasks to run at specified intervals.
    Returns:
    None
    """
    logging.info("Setting up schedule...")
    schedule.every(30).seconds.do(job, conn)  # Adjust this to every minute or as needed

    while True:
        schedule.run_pending()
        time.sleep(1)
