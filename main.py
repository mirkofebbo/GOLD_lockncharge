import requests
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()

LOCKNCHARGE_URL             = os.getenv("LOCKNCHARGE_URL")
LOCKNCHARGE_ID              = os.getenv("LOCKNCHARGE_ID")
LOCKNCHARGE_CLIENT_ID       = os.getenv("LOCKNCHARGE_CLIENT_ID")
LOCKNCHARGE_CLIENT_SECRET   = os.getenv("LOCKNCHARGE_CLIENT_SECRET")

def load_local_token():
    file_path = "./data/token.json"

    try:
        # Check if the file exists + load
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        # else create an empty file
        data = {"access_token": None, "expires": None}
        with open(file_path, 'w') as file:
            json.dump(data, file)

    return data

def check_token_expiry(token_data):

    if token_data['access_token'] is None:
        return False
    elif token_data['expires'] < time.time():
        return False
    else:
        return True
    
def save_token(token_data):
    file_path = "data/token.json"

    with open(file_path, 'w') as file:
        json.dump(token_data, file)

def get_token():
    url = LOCKNCHARGE_URL + "token"
    data = {
        "client_id": LOCKNCHARGE_CLIENT_ID,
        "client_secret": LOCKNCHARGE_CLIENT_SECRET
    }

    response = requests.post(url, data=data)

    token = response.json()
    return token

def main():
    local_token = load_local_token()
    if not check_token_expiry(local_token):
        print("Token expired or not found, fetching new token...")
        token_data = get_token()
        token_data['expires'] = time.time() + token_data['expires']
        save_token(token_data)

    else:
        print("Using existing valid token.")
    # token_data = get_token()
    
    


if __name__ == "__main__":
    main()
