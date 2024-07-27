"""
© 2024 Nirnajan Shrestha. All rights reserved.
"""

import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
import pandas as pd
from langchain_community.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain_community.llms import HuggingFaceHub
from InstructorEmbedding import INSTRUCTOR
import embeddingandInsert
import responseGeneration


# def handle_userinput(user_question):
#     response = st.session_state.conversation({'question': user_question})
#     st.session_state.chat_history = response['chat_history']

#     for i, message in enumerate(st.session_state.chat_history):
#         if i % 2 == 0:
#             st.write(user_template.replace(
#                 "{{MSG}}", message.content), unsafe_allow_html=True)
#         else:
#             st.write(bot_template.replace(
#                 "{{MSG}}", message.content), unsafe_allow_html=True)

def handle_userinput(user_question):
    
    st.info("We are getting your answer please wait....")
    response_messages = responseGeneration.generate_response(user_question)
    if response_messages:
        st.write(response_messages)   
    else:
        st.error("Error generating response. Please try again.")


def main():
    load_dotenv()
    try:
        print("Creating Table")
        embeddingandInsert.create_table_if_not_exists()

    except:
        print("Error connecting to database")
    
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                st.info("Extacting pdf data ")
                text_per_page,pdf_title = embeddingandInsert.extract_text_from_pdf(pdf_docs)
                st.info("Extacting pdf complete ")
                # get the text chunks
                st.info("Embedding pdf data ")
                embeddings = embeddingandInsert.query(text_per_page)
                st.info("Embedding pdf complete ")
                df = pd.DataFrame({'text_content': text_per_page, 'embedding': embeddings,'document_title':pdf_title})
                st.info("inserting pdf data into postgres database ")
                
                isCompleted = embeddingandInsert.insert_embeddings_into_db(df)
                
                if isCompleted:
                    st.info("inserting pdf data into postgres database complete")
                    st.success('Processing complete!')
                else:
                    st.error('Processing Error!')

if __name__ == '__main__':
    main()
