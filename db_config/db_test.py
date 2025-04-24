import psycopg2
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname="pulsecheck_db",
        user="postgres",
        password=os.getenv("PG_ADMIN_PWD"),
        host="localhost",
        port="5432"
    )

# Test the connection
if __name__ == "__main__":
    try:
        conn = get_connection()
        print("Connection successful!")
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")
