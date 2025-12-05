import requests
import logging
import time
from datetime import datetime

from lockncharge_api.auth import LocknChargeAuth

LOG_FILE_NAME = 'app.log'

logging.basicConfig(
    level=logging.DEBUG,
    filename=LOG_FILE_NAME,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )

logger = logging.getLogger(__name__)

class LocknChargeAPI:
    def __init__(self, api_url: str, station_id:str, client_id:str, client_secret:str):
        logger.info("[API] Initializing LocknChargeAPI.")
        self.url:str                = api_url
        self.id:str                 = station_id
        self.auth:LocknChargeAuth   = LocknChargeAuth(api_url, client_id, client_secret)
        self.token:str              = self.auth.get_token()

    #==== FUNCTION TO MOVE ====
    def get_assigned_bays(self, bays:dict):
        """ BAY JSON EXEMPLE
            {
                "id": "S-70:b3:d5: 8f: 92:ff-00000000898cee65_B-1", 
                "bayNumber": 1, 
                "stationId": "S-70:b3:d5: 8f: 92:ff-00000000898cee65", 
                "name": "Bay 1", 
                "locked": True, 
                "offline": False, 
                "assigned": False, 
                "assignedUserId": None, 
                "tags": ["macbook"]
            },
        """
        assigned_bays:list = []
        for bay in bays["items"]:
            if bay["assigned"]:
                assigned_bays.append(bay)

        return assigned_bays 
    
    def get_current_users(self, assigned_bays:list):
        # Using the assignedUserId we can extract the user info
        current_users = []
    
        for bay in assigned_bays:
            
            user_id = bay["assignedUserId"]
            user_info = self.get_user(user_id)
            user = {
                    "username": user_info["name"],
                    "user_id": user_id,
                    "bay_number": bay["bayNumber"],
                    "assigned_time_utc": time.time(),
                    "assigned_time_human": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "returned_time_utc": "NULL",
                    "returned_time_human": "NULL"
                }
            current_users.append(user)
        return current_users
        
    #==== API CALS ====
    def get_connection_status(self):
        # we can get alot of info from this call: id, name connected, firmwareVersion, update, lockdown, tags, nodeId
        # But we are only interested to know if the locker is connected.
        url:str = f'{self.url}stations/{self.id}'
        headers:dict = {
            'Accept': 'application/json',
            'Authorization': f"Bearer {self.token}"
        }

        response:requests.Response = requests.get(url, headers=headers)
        data:dict = response.json()
        
        return data["connected"]
    
    def get_bays(self):
        url:str = f'{self.url}bays?tags=macbook'
        headers:dict = {
            'Accept': 'application/json',
            'Authorization': f"Bearer {self.token}"
        }

        response:requests.Response = requests.get(url, headers=headers)
        data:dict = response.json()
        
        return data

    def get_user(self, user_id: str):

        url:str = f'{self.url}station-users/{user_id}'
        headers:dict = {
            'Accept': 'application/json',
            'Authorization': f"Bearer {self.token}"
        }

        response:requests.Response = requests.get(url, headers=headers)
        data:dict = response.json()
        
        return data

