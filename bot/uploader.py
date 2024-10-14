import requests
import logging
import os

# Set up logging
logging.basicConfig(
    filename='../logs/bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def download_file(url, save_path):
    """Downloads a file from the given URL and saves it to the specified path."""
    try:
        logger.info(f"Starting download from {url}")
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            logger.info(f"Download completed: {save_path}")
            print(f"Download completed: {save_path}")
        else:
            logger.error(f"Failed to download file. Status code: {response.status_code}")
            print(f"Failed to download file. Status code: {response.status_code}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
