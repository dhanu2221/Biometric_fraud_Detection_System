import chromadb

CHROMA_PATH = "./chroma_store"

def get_client():
    return chromadb.PersistentClient(path=CHROMA_PATH)

def get_or_create_collection(name: str):
    client = get_client()
    return client.get_or_create_collection(name=name)