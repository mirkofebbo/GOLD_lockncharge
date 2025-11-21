import os   
from dotenv import load_dotenv
from lockncharge_api.api import LocknChargeAPI

load_dotenv()

LOCKNCHARGE_URL             = os.getenv("LOCKNCHARGE_URL")
LOCKNCHARGE_ID              = os.getenv("LOCKNCHARGE_ID")
LOCKNCHARGE_CLIENT_ID       = os.getenv("LOCKNCHARGE_CLIENT_ID")
LOCKNCHARGE_CLIENT_SECRET   = os.getenv("LOCKNCHARGE_CLIENT_SECRET")

api = LocknChargeAPI(LOCKNCHARGE_URL, LOCKNCHARGE_ID, LOCKNCHARGE_CLIENT_ID, LOCKNCHARGE_CLIENT_SECRET)
def main():

    status:bool = api.get_connection_status()

    print(status)
    
if __name__ == "__main__":
    main()
