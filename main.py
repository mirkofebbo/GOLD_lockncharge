import os   
import logging
from dotenv import load_dotenv
from lockncharge_api.api import LocknChargeAPI

LOG_FILE_NAME = 'app.log'

logging.basicConfig(
    level=logging.DEBUG,
    filename=LOG_FILE_NAME,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )

logger = logging.getLogger(__name__)

load_dotenv()

LOCKNCHARGE_URL             = os.getenv("LOCKNCHARGE_URL")
LOCKNCHARGE_ID              = os.getenv("LOCKNCHARGE_ID")
LOCKNCHARGE_CLIENT_ID       = os.getenv("LOCKNCHARGE_CLIENT_ID")
LOCKNCHARGE_CLIENT_SECRET   = os.getenv("LOCKNCHARGE_CLIENT_SECRET")

api = LocknChargeAPI(LOCKNCHARGE_URL, LOCKNCHARGE_ID, LOCKNCHARGE_CLIENT_ID, LOCKNCHARGE_CLIENT_SECRET)
def main():

    status:bool = api.get_connection_status()
    bays:dict = api.get_bays()
    assigned_bays = api.get_assigned_bays(bays)
    user = api.get_user(assigned_bays[0]["assignedUserId"])
    print(user)
    # logger.info(f"[MAIN] Connection status: {status}")
    
if __name__ == "__main__":
    main()