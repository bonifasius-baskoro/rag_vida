import chromadb
from dotenv import load_dotenv
import os
load_dotenv() 

host = os.environ.get("CHROMADB_HOST")
port = os.environ.get("CHROMADB_PORT")
def connect_vectordb():
    chroma_client = chromadb.HttpClient(
    host="34.101.175.114",
    port=8000  
    )
    return chroma_client

def check_connection_vectordb():
    try: 
        chroma_client = chromadb.HttpClient(
        host="34.101.175.114",
        port=8000)
        return True
    except: 
        return False