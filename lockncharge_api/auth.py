import requests
import time
import logging
from datetime import datetime
from .utils import save_json, load_json

LOG_FILE_NAME = 'app.log'

logging.basicConfig(
    level=logging.DEBUG,
    filename=LOG_FILE_NAME,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )

logger = logging.getLogger(__name__)

class LocknChargeAuth:
    def __init__(self, api_url: str, client_id: str, client_secret: str):
        
        self.url:str = api_url
        self.id:str  = client_id
        self.secret:str  = client_secret

        file_path = "./data/token.json"
        self.token_data:dict = load_json(file_path)
        
        if not bool(self.token_data):
            logger.debug(f"[AUTH] No local token")
            self.token_data:dict = self.api_get_token()
            save_json(self.token_data, file_name)

        try:    
            if not self.check_token_expiry():
                self.token_data:dict = self.api_get_token()
                file_name:str = "token.json"
                save_json(self.token_data, file_name)


        except Exception as e:
            logger.error(f"[AUTH] Error getting token from API: {e}")
        
        logger.debug(f"[AUTH] Token expires: {datetime.fromtimestamp(self.token_data['expires'])}")

    def check_token_expiry(self):

        if self.token_data['access_token'] is None:
            logger.debug("[AUTH] No token found.")
            return False
        elif self.token_data['expires'] < time.time():
            logger.debug("[AUTH] Token expired.")
            return False
        else:
            return True

    def api_get_token(self):  
        url:str = self.url + "token"
        data:dict = {
            "client_id": self.id,
            "client_secret": self.secret
        }

        response:requests.Response = requests.post(url, data=data)

        token:dict = response.json()
        return token
    
    def get_token(self):

        if not self.check_token_expiry():
            print("Token expired or not found, fetching new token...")
            self.token_data = self.get_token()
            file_name:str = "token.json"
            save_json(self.token_data, file_name)
        
        return self.token_data["access_token"]