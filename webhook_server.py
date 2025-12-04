from flask import Flask, request, jsonify
from lockncharge_api.db_managment import DatabaseManager
from lockncharge_api.api import LocknChargeAPI
import os
from dotenv import load_dotenv
import logging

load_dotenv()
LOG_FILE_NAME = 'app.log'

logging.basicConfig(
    level=logging.DEBUG,
    filename=LOG_FILE_NAME,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )
db = DatabaseManager('./data/example.db')

LOCKNCHARGE_URL             = os.getenv("LOCKNCHARGE_URL")
LOCKNCHARGE_ID              = os.getenv("LOCKNCHARGE_ID")
LOCKNCHARGE_CLIENT_ID       = os.getenv("LOCKNCHARGE_CLIENT_ID")
LOCKNCHARGE_CLIENT_SECRET   = os.getenv("LOCKNCHARGE_CLIENT_SECRET")

api = LocknChargeAPI(LOCKNCHARGE_URL, LOCKNCHARGE_ID, LOCKNCHARGE_CLIENT_ID, LOCKNCHARGE_CLIENT_SECRET)

app = Flask(__name__)

@app.post("/lockncharge/webhook")
def webhook():
    event = request.json

    logging.info(f"Received webhook: {event}")

    event_type = event.get("event")
    print(event_type)
    # # --- HANDLE EVENTS ---
    # if event_type == "bayAssigned":
    #     user_id = event.get("assignedUserId")
    #     bay_id = event.get("bayId")

    #     user_info = api.get_user(user_id)

    #     db.add_entry("RHB115", {
    #         "username": user_info["name"],
    #         "user_id": user_id,
    #         "bay_number": bay_id,
    #         "assigned_time_utc": event.get("time"),
    #         "assigned_time_human": "",
    #         "returned_time_utc": "",
    #         "returned_time_human": ""
    #     })

    #     logging.info(f"User {user_id} assigned to {bay_id}")

    # elif event_type == "bayUnassigned":
    #     user_id = event.get("assignedUserId")
    #     db.mark_returned(user_id)  # You will implement this
    #     logging.info(f"User {user_id} returned laptop")

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
