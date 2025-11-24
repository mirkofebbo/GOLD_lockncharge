import json
import logging


LOG_FILE_NAME = 'app.log'

logging.basicConfig(
    level=logging.DEBUG,
    filename=LOG_FILE_NAME,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )

logger = logging.getLogger(__name__)

def save_json(data:dict, file_name:str):
    file_path:str = f"data/{file_name}"
    
    with open(file_path, 'w') as file:
        json.dump(data, file)

    logger.info(f"[UTIL] Saved Jason: {file_path}")


def load_json(file_path):

    try:
        # Check if the file exists + load
        logger.debug(f"[UTIL] Loading Json: {file_path}")
        with open(file_path, 'r') as file:
            data:dict = json.load(file)
    except FileNotFoundError:
        # else create an empty file
        data:dict = {}
        with open(file_path, 'w') as file:
            json.dump(data, file)
        logger.debug(f"[UTIL] Creating Json: {file_path}")
