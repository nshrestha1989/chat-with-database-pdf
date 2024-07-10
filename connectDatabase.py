"""
© 2024 Nirnajan Shrestha. All rights reserved.
"""


import psycopg2
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv(), override=True)

# Retrieve database connection details from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Construct the connection string
conn_string = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}"

try:
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(conn_string)

    # Create a cursor object using the connection
    cursor = conn.cursor()

    # Example query execution
    insert_statement = """
    INSERT INTO users (text_content, embedding)
    VALUES (%s, %s, %s);
    """

    # Execute the INSERT statement
    cursor.execute(insert_statement)
    db_version = cursor.fetchone()
    print(f"Connected to {db_version}")

    # Close cursor and connection
    cursor.close()
    conn.close()

except psycopg2.Error as e:
    print("Error connecting to PostgreSQL:", e)
