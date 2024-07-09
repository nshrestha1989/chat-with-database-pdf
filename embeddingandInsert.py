import requests
import psycopg2
import os
from dotenv import load_dotenv, find_dotenv
import pandas as pd
from psycopg2.extras import Json
import fitz  # PyMuPDF
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

# Load environment variables from .env file
load_dotenv(find_dotenv(), override=True)

# Hugging Face API credentials and model information
model_id =os.getenv("MODEL_ID")
hf_token = os.getenv("HC_TOKEN")

api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {hf_token}"}

def query(texts):
    response = requests.post(api_url, headers=headers, json={"inputs": texts, "options": {"wait_for_model": True}})
    return response.json()
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def extract_text_from_pdf(pdf_docs):
    text_per_page = []
    for pdf in pdf_docs:
    # Open the provided PDF file
        pdf_reader = PdfReader(pdf)
        # Iterate through each page of the document
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            text_per_page.append(page_text)
        return text_per_page


def insert_embeddings_into_db(df):
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
        INSERT INTO public.embeddings_table (text_content, embedding)
        VALUES (%s, %s);
        """

        # Loop through each row in the DataFrame and insert into the database
        for index, row in df.iterrows():
            text_content = row['text_content']
            embedding = row['embedding']
            cursor.execute(insert_statement, (text_content, Json(embedding)))

        # Commit changes to the database
        conn.commit()
        print("Data successfully inserted into PostgreSQL")

    except psycopg2.Error as e:
        print(f"Error inserting data into PostgreSQL: {e}")

    finally:
        # Close cursor and connection
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
