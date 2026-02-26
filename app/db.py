import chromadb

CHROMA_HOST = "127.0.0.1"
CHROMA_PORT = 8000

def get_client():
    return chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

def get_or_create_collection(name: str):
    client = get_client()
    return client.get_or_create_collection(name=name)