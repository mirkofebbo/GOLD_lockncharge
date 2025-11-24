import os   
from dotenv import load_dotenv
from lockncharge_api.auth import LocknChargeAuth

load_dotenv()

LOCKNCHARGE_URL             = os.getenv("LOCKNCHARGE_URL")
LOCKNCHARGE_ID              = os.getenv("LOCKNCHARGE_ID")
LOCKNCHARGE_CLIENT_ID       = os.getenv("LOCKNCHARGE_CLIENT_ID")
LOCKNCHARGE_CLIENT_SECRET   = os.getenv("LOCKNCHARGE_CLIENT_SECRET")

auth = LocknChargeAuth(LOCKNCHARGE_URL, LOCKNCHARGE_CLIENT_ID, LOCKNCHARGE_CLIENT_SECRET)

def main():

    token:str = auth.get_token()
    print(token)
    
if __name__ == "__main__":
    main()
