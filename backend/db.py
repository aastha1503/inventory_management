import pymysql
from dotenv import load_dotenv
from pymysql.err import MySQLError
import os

load_dotenv()

def create_connection():
    try:
        connection = pymysql.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )

        # if connection.is_connected():
        #     print("✅ Connected to MySQL Database")

        return connection

    except MySQLError as e:
        print(f" Error while connecting to MySQL: {e}")
        return None
    
db_connect = create_connection()    