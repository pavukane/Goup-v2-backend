import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv('.flaskenv')


def request_connection():
    # init mysql db
    conn = mysql.connector.connect(
        host=os.environ["HOST"],
        port=os.environ["PORT"],
        user=os.environ["USER"],
        password=os.environ["PASSWORD"]
    )
    return conn


def request_cursor(conn):
    return conn.cursor()




