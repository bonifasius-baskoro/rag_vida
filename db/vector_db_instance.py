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

def get_collection(collection="slik_test"):
    print("get collection vector db...")
    client = connect_vectordb()
    collection = client.get_collection("slik_test")
    return collection

def query_vector_db(query, n_results = 10):
    print("Query searching for ", query)
    collection = get_collection()
    results = collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
    return results

def check_connection_vectordb():
    try: 
        chroma_client = chromadb.HttpClient(
        host="34.101.175.114",
        port=8000)
        return True
    except: 
        return False