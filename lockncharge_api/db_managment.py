import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=DB_PASSWORD
)

print(mydb)