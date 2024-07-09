Follow this to install pgvector in you local computer:
https://github.com/pgvector/pgvector

run command as Admin

python version 3.9
pip install -r requirements.txt
streamlit run app.py

#rename .evnExample to .env and fill in credentials

#huggginface api

its using huggingface api , use MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2" in .env file
generate token from huggingface  HC_TOKEN =xxxhuggingface-tokenxxx

.env example
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="AIData"
DB_USER="postgres"
DB_PASSWORD="1234"
MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
HC_TOKEN = "xxxxxx"


more documenation coming soon!!!!!