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
# cursor.execute("CREATE TABLE RHB115(username TEXT, user_id TEXT, bay_number INTEGER, assigned_time_utc REAL, assigned_time_human DATETIME, returned_time_utc REAL, returned_time_human DATETIME)")

# # # add dummy data
# # cursor.execute("INSERT INTO RHB115 (username, user_id, bay_number, assigned_time_utc, assigned_time_human, returned_time_utc, returned_time_human) VALUES (?, ?, ?, ?, ?, ?, ?)", ("testuser", "user123", 1, 1622548800.0, "2021-06-01 12:00:00", None, None))
# # conn.commit()
# # conn.close()

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    # ==== DATABASE METHODS =====
    def create_table(self, table_name: str, schema: str):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})")
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
        keys = ', '.join(parsed_data.keys())
        question_marks = ', '.join(['?'] * len(parsed_data))
        values = tuple(parsed_data.values())
        query = f"INSERT INTO {table_name} ({keys}) VALUES ({question_marks})"
        self.execute_query(query, values)
        logger.info(f"[DB] Entry booked'{table_name}|bay-{parsed_data["bay_number"]}, at {parsed_data["book_timestamp"]}")


    def update_entry_from_bay(self, table_name:str, bay: int, timestamp: str):

        query = f"UPDATE {table_name} SET return_timestamp = ? WHERE bay_number = ? AND return_timestamp = ''"
        values = (timestamp, bay)
        self.execute_query(query, values)
        logger.info(f"[DB] Entry returned to {table_name}|bay-{bay}, at: {timestamp}") 