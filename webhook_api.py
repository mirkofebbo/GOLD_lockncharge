from flask import Flask, request, jsonify
from lockncharge_api.db_managment import DatabaseManager
from lockncharge_api.api import LocknChargeAPI
import os
from dotenv import load_dotenv
import logging

LOG_FILE_NAME = 'app.log'

logging.basicConfig(
    level=logging.DEBUG,
    filename=LOG_FILE_NAME,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

db = DatabaseManager('./data/example.db')

LOCKNCHARGE_URL             = os.getenv("LOCKNCHARGE_URL")
LOCKNCHARGE_ID              = os.getenv("LOCKNCHARGE_ID")
LOCKNCHARGE_CLIENT_ID       = os.getenv("LOCKNCHARGE_CLIENT_ID")
LOCKNCHARGE_CLIENT_SECRET   = os.getenv("LOCKNCHARGE_CLIENT_SECRET")

# api = LocknChargeAPI(LOCKNCHARGE_URL, LOCKNCHARGE_ID, LOCKNCHARGE_CLIENT_ID, LOCKNCHARGE_CLIENT_SECRET)
database_manager = DatabaseManager('./data/example.db')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """
    Go to localhost:5000 to see a message
    """
    return ('Ta mere la pute.', 200, None)


@app.route("/webhook", methods=["POST"])
def lcn_webhook():
    # Get JSON payload from LocknCharge webhook
    payload:dict = request.get_json(silent=True)

    print("=== Incoming LocknCharge Webhook ===")
    print(payload)
    event_type:str = payload["type"] 

    match event_type:
        case "BAY_CREDS_CACHED":
            # Bay {bay} reserved on station {station}
            print("")
        case "BAY_CREDS_CLEARED":
            # Bay {bay} accessed on station {station}.
            print("BAY_CREDS_CLEARED")
        case "BAY_CLOSED":
            # Bay {bay} closed on station {station}.
            print("BAY_CLOSED")
        case "BAY_STUCK":
            # Bay {bay} stuck on station {station}.
            print("BAY_STUCk")
        case "BAY_BREACH":
            # Bay {bay} breached on station {station}.
            print("BAY_BREACH")
        case "BAY_TMPBAN":
            # Bay {bay} was locked out due to incorrect access attempts on station {station}.
            print("BAY_TMPBAN")
    return jsonify({"status": "received"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=1)
