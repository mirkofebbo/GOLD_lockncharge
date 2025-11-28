import sqlite3

conn = sqlite3.connect('./data/example.db')  # Creates a new database file if it doesn’t exist
cursor = conn.cursor()
cursor.execute("CREATE TABLE RHB115(username TEXT, user_id TEXT, bay_number INTEGER, assigned_time_utc REAL, assigned_time_human DATETIME, returned_time_utc REAL, returned_time_human DATETIME)")

# add dummy data
cursor.execute("INSERT INTO RHB115 (username, user_id, bay_number, assigned_time_utc, assigned_time_human, returned_time_utc, returned_time_human) VALUES (?, ?, ?, ?, ?, ?, ?)", ("testuser", "user123", 1, 1622548800.0, "2021-06-01 12:00:00", None, None))
conn.commit()
conn.close()