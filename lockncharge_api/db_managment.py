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
    def add_entry(self, table_name: str, data: dict):  
        keys = ', '.join(data.keys())
        question_marks = ', '.join(['?'] * len(data))
        values = tuple(data.values())
        query = f"INSERT INTO {table_name} ({keys}) VALUES ({question_marks})"
        self.execute_query(query, values)
        logger.info(f"[DB] Entry added to '{table_name}': {data}")
