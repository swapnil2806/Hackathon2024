import os
import streamlit as st

from util import *
import openai
from langchain.llms import OpenAI
from prompt_txn import *
import string  # Add this line to import the string module
import pandas as pd
import numpy as np
import datetime
import random


image_path = 'ChatBot1.png'
openai.api_key = "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"
os.environ["OPENAI_API_KEY"] = "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"
MODEL = "gpt-3.5-turbo"
llm = OpenAI(model_name=MODEL, temperature=0)

df = pd.read_csv('TxnDetails.csv')
df['Transaction_date'] = pd.to_datetime(df['Transaction_date'])
df['Benename'] = df['Benename'].str.lower()

openai.api_key = os.getenv("OPENAI_API_KEY")

def process_documents_and_answer_question(documents, question):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    document_objects = []

    for document_text in documents:
        chunks = text_splitter.split_text(document_text)
        document_objects.extend([DocumentObject(chunk) for chunk in chunks])
    
    embeddings = CustomOpenAIEmbeddings(API_KEY)
    db = Chroma.from_documents(document_objects, embeddings)
    
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 2})
    
    qa = RetrievalQA.from_chain_type(llm=OpenAI(api_key=API_KEY), chain_type="base", retriever=retriever, return_source_documents=True)
    
    result = qa({"query": question})
    return result

# Modify the `exec` usage to match how results are generated
def textToSQL(question, documents):
    formatted_prompt = query_prompt_txn.format(question=question)
    messages = [{"role": "user", "content": formatted_prompt}]
    
    try:
        response = openai.ChatCompletion.create(model=MODEL, messages=messages)
        llm_out = response.choices[0].message['content']
        
        local_vars = {'df': documents}  # Pass 'documents' DataFrame as 'df'
        exec(llm_out, globals(), local_vars)
        
        # Adjust this line based on how 'llm_out' assigns or returns its result
        answer = local_vars.get('func')()  # If 'func' returns the desired result
        return answer
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
     # CSS to inject contained in a multi-line string
    background = """
        <style>
        h1 {
            color: #ADD8E6;
        }
        .stTextInput>div>div>input {
            color: black;
        }
        .stButton>button {
            border: 2px solid #ADD8E6; /* Light Blue */
            background-color: #ADD8E6; /* Light Blue */
            color: white;
            padding: 10px 24px;
            cursor: pointer;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #BFEFFF; /* Lighter Blue */
            color: white;
        }
        </style>
    """


    st.markdown(background, unsafe_allow_html=True)
    st.markdown("# AI Crafters' 💬")
    st.image(image_path, width=700)
    st.title("Transaction Query Processor")
    questionAsk = st.text_input("Enter your transaction query:", "")

    if st.button("Process Query"):
      if questionAsk:
          # Call the textToSQL function with the question and df
          try:
              reply = textToSQL(questionAsk,df)
              if reply is not None:
                  # Display the answer
                  st.success("Query processed successfully.")
                  st.write(reply)
              else:
                  st.error("No answer could be generated for the query.")
          except Exception as e:
              st.error(f"An error occurred: {str(e)}")
      else:
          st.error("Please enter a query to process.")


if __name__ == "__main__":
    main()
