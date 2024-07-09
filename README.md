### README for Streamlit PDF Chat Application

#### Overview
This application allows users to interactively chat with content extracted from multiple PDF documents. Users can upload their PDF files, which the application processes to extract text and generate responses based on user queries.

#### Features
- Upload and process multiple PDF documents.
- Extract text from PDFs and embed them using machine learning models.
- Store embeddings in a PostgreSQL database.
- Generate conversational responses using embedded document content.

#### Setup

1. **Clone the Repository**
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install Dependencies**
    ```sh
    pip install -r requirements.txt
    ```

3. **Environment Variables**
    - Rename `.envExample` to `.env` in the project root.
    - Add the following variables to the `.env` file:
    ```sh
    DB_HOST="localhost"
    DB_PORT="5432"
    DB_NAME="AIData"
    DB_USER="postgres"
    DB_PASSWORD="1234"
    MODEL_ID="sentence-transformers/all-MiniLM-L6-v2"
    HC_TOKEN="xxxxxx"
    ```

4. **Install `pgvector` Extension**
    Follow the instructions to install `pgvector` in your local PostgreSQL setup:
    [pgvector GitHub Repository](https://github.com/pgvector/pgvector)

    To install `pgvector` on your local computer:
    - **macOS**:
        ```sh
        brew install pgvector/tap/pgvector
        ```

    - **Linux**:
        ```sh
        # Clone the repository
        git clone https://github.com/pgvector/pgvector.git
        cd pgvector

        # Make and install
        make
        sudo make install
        ```

    - **Windows**:
        Follow the detailed guide on the [pgvector GitHub page](https://github.com/pgvector/pgvector).

    - **Enable pgvector in PostgreSQL**:
        ```sh
        psql -d mydatabase -c "CREATE EXTENSION vector;"
        ```

5. **Run the Application**
    ```sh
    streamlit run app.py
    ```

#### Requirements

The required libraries and their versions are listed in `requirements.txt`:

```
langchain==0.0.184
PyPDF2==3.0.1
python-dotenv==1.0.0
streamlit==1.18.1
openai==0.27.6
htmltemplate
InstructorEmbedding==1.0.1
sentence-transformers==2.2.2
altair==4
```

To install the dependencies, run:
```sh
pip install -r requirements.txt
```

**Python Version**: Ensure you are using Python 3.9

#### Usage

1. **Upload PDFs**
    - In the sidebar, click "Upload your PDFs here and click on 'Process'".
    - Select one or more PDF files to upload.
    - Click the "Process" button to extract and embed text from the PDFs.

2. **Ask Questions**
    - Enter your question in the text input field at the top of the page.
    - The application will display responses generated based on the content of the uploaded PDFs.

3. **View Chat History**
    - The chat history is displayed interactively, showing the user’s questions and the system’s responses.

#### Hugging Face API

- This application uses Hugging Face's API to generate embeddings.
- Set `MODEL_ID="sentence-transformers/all-MiniLM-L6-v2"` in your `.env` file.
- Generate a Hugging Face token and set `HC_TOKEN="your_huggingface_token"` in your `.env` file.

#### Gemini API by Google

- This application uses the Gemini API by Google for response generation.
- Ensure you have access to the Gemini API and set up the necessary environment variables.

**Steps to set up Gemini API:**

1. **Create a Google Cloud Project**
    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - Create a new project or select an existing project.

2. **Enable Gemini API**
    - In the Google Cloud Console, navigate to "APIs & Services" > "Library".
    - Search for "Gemini API" and click "Enable".

3. **Set Up Authentication**
    - Install and initialize the Google Cloud SDK:
      ```sh
      curl https://sdk.cloud.google.com | bash
      exec -l $SHELL
      gcloud init
      ```

    - Authenticate your user account:
      ```sh
      gcloud auth application-default login
      ```

4. **Set Environment Variables**
    - Add the following variables to your `.env` file:
    ```sh
    GEMINI_PROJECT_ID="your_google_cloud_project_id"
    GEMINI_LOCATION="us-central1"
    ```

5. **Install Google Cloud Client Library**
    ```sh
    pip install google-cloud
    ```

#### .env Example

Here's an example `.env` file:

```sh
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="AIData"
DB_USER="postgres"
DB_PASSWORD="1234"
MODEL_ID="sentence-transformers/all-MiniLM-L6-v2"
HC_TOKEN="xxxxxx"
GEMINI_PROJECT_ID="your_google_cloud_project_id"
GEMINI_LOCATION="us-central1"
```

#### Code Structure

- **app.py**: Main application file to run the Streamlit app.
- **embeddingandInsert.py**: Contains functions to extract text from PDFs, generate embeddings, and insert them into the PostgreSQL database.
- **responseGeneration.py**: Handles the generation of responses based on user input by querying the database and using machine learning models.

#### Functions

- **handle_userinput(user_question)**
    - Processes user input and generates a response based on embedded document content.

- **main()**
    - Sets up the Streamlit application layout, handles file uploads, and processes PDFs.

- **get_pdf_text(pdf_docs)**
    - Extracts text from each page of the uploaded PDFs.

- **extract_text_from_pdf(pdf_docs)**
    - Extracts and returns text content from the uploaded PDF documents.

- **insert_embeddings_into_db(df)**
    - Inserts extracted text and corresponding embeddings into a PostgreSQL database.

- **generate_response(user_input)**
    - Generates a response based on user input by querying the PostgreSQL database and formatting the retrieved data for response generation.

#### Database Integration

- Uses `psycopg2` to connect and interact with a PostgreSQL database.
- Stores text content and corresponding embeddings in a table named `embeddings_table`.

#### Troubleshooting

- **Database Connection Issues**: Verify the database credentials in the `.env` file and ensure the database is running.
- **API Errors**: Ensure the Hugging Face token and Google Cloud credentials are valid and have the necessary permissions.

For any issues or contributions, please open an issue or create a pull request on the repository.

#### More Documentation

More documentation and detailed guides will be coming soon! Stay tuned.