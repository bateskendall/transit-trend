import requests
from typing import Optional

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