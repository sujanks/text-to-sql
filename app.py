import os
import streamlit as st
from sqlalchemy import create_engine, MetaData
from llama_index import LLMPredictor, ServiceContext, VectorStoreIndex
from langchain_community.utilities import SQLDatabase
from llama_index.core.indices.struct_store.sql_query import SQLTableRetrieverQueryEngine
from llama_index.core.objects import SQLTableNodeMapping, ObjectIndex, SQLTableSchema
from langchain_openai import OpenAI


# Set your OpenAI API key here
os.environ["OPENAI_API_KEY"] = st.secrets.openai_key

# Directly using database connection details
host = "localhost"
user = "postgres"
password = "password"
database = "hr"

# Setup database connection
db_uri = f"postgresql+psycopg2://{user}:{password}@{host}:5432/{database}"
db = SQLDatabase.from_uri(db_uri)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

# Streamlit app layout  
st.title('SQL Chatbot')

# User input
user_query = st.text_area("Enter your SQL-related query:", "List Top 10 Employees by Salary?")

if st.button('Submit'):
    #try:
        # Processing user input
        #response = agent_executor.invoke(user_query)
        #response = agent_executor.invoke({"query": user_query})
        #if st.button('Submit'):
    try:
        # Processing user input
        response = agent_executor.invoke({
            "agent_scratchpad": "",  # Assuming this needs to be an empty string if not used
            "input": user_query  # Changed from "query" to "input"
        })
        st.write("Response:")
        st.json(response)  # Use st.json to pretty print the response if it's a JSON
    except Exception as e:
        st.error(f"An error occurred: {e}")