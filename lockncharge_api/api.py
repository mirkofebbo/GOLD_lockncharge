import requests

class LocknChargeAPI:
    def __init__(self, api_url: str):
        print('Started API')
        self.url:str = api_url
        self.token:str = None
    

