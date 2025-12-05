import sqlite3
import logging

LOG_FILE_NAME = 'app.log'

logging.basicConfig(
    level=logging.DEBUG,
    filename=LOG_FILE_NAME,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# conn = sqlite3.connect('./data/example.db')  # Creates a new database file if it doesn’t exist
# cursor = conn.cursor()
# cursor.execute(
#     "CREATE TABLE IF NOT EXISTS RHB115 ("
#     "user_id TEXT, username TEXT, bay_number INTEGER, book_timestamp TEXT, return_timestamp TEXT)"
# )

# # add dummy data
# cursor.execute("INSERT INTO RHB115 (user_id, username, bay_number, book_timestamp, return_timestamp) VALUES (?, ?, ?, ?, ?)", ("3e410120-6c9a-40b1-a16c-69a15cb9e85e", "temp", 1, "2021-06-01 12:00:00", None))
# conn.commit()
# conn.close()

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    # ==== DATABASE METHODS =====
    def create_table(self, table_name: str, schema: str):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} ("
                "user_id TEXT, username TEXT, bay_number INTEGER, book_timestamp TEXT, return_timestamp TEXT)"
            )
            conn.commit()
            conn.close()
            logger.info(f"[DB] Table '{table_name}' created or already exists.")
        except sqlite3.Error as e:
            logger.error(f"[DB] Error creating table '{table_name}': {e}")

    def execute_query(self, query: str, params: tuple = ()):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            results = cursor.fetchall()
            conn.close()
            return results
        except sqlite3.Error as e:
            logger.error(f"[DB] Database error: {e}")
            return None
        
    # ==== DATA PARSING METHODS =====
    def new_data_parsing(self, data:dict):
        formated_data = {
            "user_id": data["data"]["user"]["id"],
            "username": data["data"]["user"].get("name", data["userType"]) ,
            "bay_number": data["data"]["bay"],
            "book_timestamp": data["timestamp"],
            "return_timestamp": ""
        }
        return formated_data
    
    def add_entry(self, table_name: str, data: dict):  

        parsed_data:dict = self.new_data_parsing(data)
        print(f"[db_managment]: {parsed_data}")
        keys = ', '.join(parsed_data.keys())
        question_marks = ', '.join(['?'] * len(parsed_data))
        values = tuple(parsed_data.values())
        query = f"INSERT INTO {table_name} ({keys}) VALUES ({question_marks})"
        self.execute_query(query, values)
        logger.info(f"[DB] Entry added to '{table_name}': {parsed_data}")
