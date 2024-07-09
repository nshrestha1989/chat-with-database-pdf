"""
© 2024 Nirnajan Shrestha. All rights reserved.
"""


import psycopg2
import os
from dotenv import load_dotenv, find_dotenv
import numpy as np
from sentence_transformers import SentenceTransformer
from pgvector.psycopg2 import register_vector
import vertexai
import vertexai.preview.generative_models as generative_models

import embeddingandInsert
def generate(messages):
    vertexai.init(project=os.getenv("GEMINI_PROJECT_ID"), location=os.getenv("GEMINI_LOCATION"))
    model = generative_models.GenerativeModel(
        "gemini-1.5-pro-001",
    )
    
    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 0.95,
    }
    
    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
    
    responses = model.generate_content(
        messages,
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )
    temp =[]
    for response in responses:
        temp.append(response.text)
    return temp

# Load environment variables from .env file
load_dotenv(find_dotenv(), override=True)


# Retrieve database connection details from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def generate_response(user_input):
    # Construct the connection string
    conn_string = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}"

    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(conn_string)

        # Register vector type with psycopg2 for pgvector
        register_vector(conn)
        
        # Generate embedding for user input
        user_embedding=embeddingandInsert.query(user_input)
        # Convert numpy array to list
        user_embedding_list = user_embedding

        # Calculate cosine similarities between user input embedding and database embeddings
        cur = conn.cursor()
        vector_data = np.array(user_embedding_list, dtype=np.float32)

        # Get the top 3 most similar documents using the KNN <=> operator
        cur.execute("SELECT text_content FROM embeddings_table ORDER BY embedding <=> %s LIMIT 3", (vector_data,))
        top3_docs = cur.fetchall()

        # Function to format messages for GenerativeModel
        def format_messages(query, relevant_passages):
            delimiter = "```"
            messages = (f"You are a chatbot designed to answer to a dental student who is preparing for adc exam in Australia, you are design to help her pass exam.Give her answer in detail . Here's some relevant information:\n"
                        f"If the passage is irrelevant to the answer, you may ignore it.\n"
                        f"QUESTION: '{query}'\n"
                        f"PASSAGES:\n\n{delimiter}\n{relevant_passages}\n{delimiter}\n\n"
                        f"ANSWER:\n")
            return messages

        # Format messages for GenerativeModel
        relevant_passages = "\n\n".join(doc[0] for doc in top3_docs)
        messages = format_messages(user_input, relevant_passages)

        return generate(messages)

    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL:", e)
        return None
    except Exception as e:
        print("Error:", e)
        return None
