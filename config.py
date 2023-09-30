import os
from dotenv import load_dotenv

load_dotenv()

# DB parameters
db_params = {
    "dbname": os.getenv("DB_NAME", "default_db_name"),
    "user": os.getenv("DB_USER", "default_user"),
    "password": os.getenv("DB_PASSWORD", "default_db_password"),
    "host": os.getenv("DB_HOST", "default_db_host"),
    "port": os.getenv("DB_PORT", "default_db_port"),
}

# Path to the static GTFS dataset
gtfs_path = "./data/gtfs/"

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