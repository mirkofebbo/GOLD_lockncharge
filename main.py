import os   
import logging
from dotenv import load_dotenv
from lockncharge_api.api import LocknChargeAPI
from lockncharge_api.utils import save_json, load_json
from lockncharge_api.db_managment import DatabaseManager

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
database_manager = DatabaseManager('./data/example.db')

def main():

    # load previous user data
    previous_user_data = load_json("./data/current_user.json")

    # add a check 
    status:bool = api.get_connection_status()
    bays:dict = api.get_bays()
    sorted_bays = sorted(bays["items"], key=lambda x: x['bayNumber'])
    save_json(sorted_bays, "bays.json")
    assigned_bays = api.get_assigned_bays(bays)
    current_user = api.get_current_users(assigned_bays)
    # database_manager.add_entry("RHB115", assigned_bays[0])
    # for i in assigned_bays:
    #     print(bay["id"])
    

    print("==== CURRENT USERS ===")
    print(current_user)

    # database_manager.check_entry_exists("RHB115", "user123", "bay_number")
    # add user to DB 
    for user in current_user:
        # database_manager.check_entry_exists("RHB115", user)
        database_manager.add_entry("RHB115", user)

    # current_user = api.get_current_users(assigned_bays)
    
    save_json(current_user, "current_user.json")
    # print("==== USERS ===")
    # print(current_user)
    # logger.info(f"[MAIN] Connection status: {status}")
    
if __name__ == "__main__":
    main()