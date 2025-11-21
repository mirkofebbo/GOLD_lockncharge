import requests
from lockncharge_api.auth import LocknChargeAuth

class LocknChargeAPI:
    def __init__(self, api_url: str, station_id:str, client_id:str, client_secret:str):
        print('Started API')
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

 