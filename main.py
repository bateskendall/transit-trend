import logging
import psycopg2
from src.automation.scheduler import setup_schedule
from config import db_params

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    # DB connection
    conn = psycopg2.connect(**db_params)

    try:
        setup_schedule(conn)  # Pass the DB connection to the scheduler
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        # Close DB connection
        logging.info("Closing database connection...")
        conn.close()