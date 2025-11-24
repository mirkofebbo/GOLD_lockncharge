import requests
import time
import json
import logging
from datetime import datetime

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

        try:
            self.token_data:dict = self.load_local_token()
        except Exception as e:
            logger.error(f"[AUTH] Error loading local token: {e}")
            self.token_data:dict = {"access_token": None, "expires": None}
        try:    
            if not self.check_token_expiry():
                self.token_data:dict = self.api_get_token()
                self.save_token()
        except Exception as e:
            logger.error(f"[AUTH] Error getting token from API: {e}")
        
        logger.debug(f"[AUTH] Token expires: {datetime.fromtimestamp(self.token_data['expires'])}")

    def load_local_token(self):
        file_path:str = "./data/token.json"

        try:
            # Check if the file exists + load
            logger.debug("[AUTH] Loading local token.")
            with open(file_path, 'r') as file:
                data:dict = json.load(file)
        except FileNotFoundError:
            # else create an empty file
            data:dict = {"access_token": None, "expires": None}
            with open(file_path, 'w') as file:
                json.dump(data, file)
            logger.debug("[AUTH] Local File created")
        return data

    def check_token_expiry(self):

        if self.token_data['access_token'] is None:
            logger.debug("[AUTH] No token found.")
            return False
        elif self.token_data['expires'] < time.time():
            logger.debug("[AUTH] Token expired.")
            return False
        else:
            return True
        
    def save_token(self):
        file_path:str = "data/token.json"
        
        with open(file_path, 'w') as file:
            json.dump(self.token_data, file)


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
            self.save_token()
        
        return self.token_data["access_token"]

