import logging
import schedule
import time
from src.data_extraction.extractor import fetch_binary_data
from src.data_transformation.transformer import process_feed
from src.data_loading.loader import store_binary_data, ensure_table_exists
from src.data_loading.tf_loader import load_trip_updates, load_vehicle_positions, load_alerts
from config import api_key, api_endpoint_urls

def job(conn) -> None:
    """Main job function to orchestrate data fetching, processing, and loading.

    Args:
        conn: The database connection object.
    """
    
    logging.info("Starting job...")
    try:
        ensure_table_exists(conn)
        
        # Loop through endpoint urls to fetch from each endpoint
        for url in api_endpoint_urls:
            binary_data = fetch_binary_data(url, api_key)
            if binary_data:
                # Store binary data
                store_binary_data([binary_data], conn)

                # Process binary data
                trip_updates, vehicle_positions, alerts = process_feed(binary_data, conn)
                
                # Load transformed data into the database
                if trip_updates:
                    load_trip_updates(trip_updates, conn)
                if vehicle_positions:
                    load_vehicle_positions(vehicle_positions, conn)
                if alerts:
                    load_alerts(alerts, conn)
            
    except Exception as e:
        logging.error(f"Error: {e}")

def setup_schedule(conn) -> None:
    """Schedules tasks to run at specified intervals.

    This function sets up a schedule for the main job function, to run at a regular interval
    (e.g., every 30 seconds).

    Args:
        conn: The database connection object.
    """
    
    logging.info("Setting up schedule...")
    schedule.every(30).seconds.do(job, conn)  # Adjust this to every minute or as needed

    while True:
        schedule.run_pending()
        time.sleep(1)
