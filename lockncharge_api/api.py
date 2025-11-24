import requests
import logging
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

