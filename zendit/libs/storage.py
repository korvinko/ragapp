from langchain_community.vectorstores import LanceDB
from langchain_community.embeddings import OllamaEmbeddings
import lancedb
import os

def getEmbeddings():
    # create the open-source embedding function
    return OllamaEmbeddings(base_url="http://localhost:11434", model="rjmalagon/gte-qwen2-7b-instruct-embed-f16")

def getVectorStore():
    # Connect to local LanceDB
    db_path = os.getenv("DATABASE_PATH")  # Adjust the path as necessary for your setup
    db = lancedb.connect(uri=db_path)

    # create the open-source embedding function
    embeddings = getEmbeddings()

    # Initialize LanceDB vector store
    vc = LanceDB(
        uri=db_path,
        embedding=embeddings,
        table_name=os.getenv("DATABASE_TABLE")
    )

    return vc


