import os
from sentence_transformers import SentenceTransformer
from .db import get_or_create_collection

kb = get_or_create_collection("fraud_kb")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

KB_DIR = "./data/kb_docs"

def index_kb():
    if not os.path.isdir(KB_DIR):
        os.makedirs(KB_DIR, exist_ok=True)

    files = [f for f in os.listdir(KB_DIR) if os.path.isfile(os.path.join(KB_DIR, f))]
    if not files:
        # No docs yet — just skip indexing
        return

    docs, ids, metas, embs = [], [], [], []
    for fname in files:
        path = os.path.join(KB_DIR, fname)
        text = open(path, "r", encoding="utf-8", errors="ignore").read().strip()
        if not text:
            continue
        docs.append(text)
        ids.append(fname)
        metas.append({"source": fname})
        embs.append(embedder.encode(text).tolist())

    if ids:
        kb.upsert(ids=ids, documents=docs, metadatas=metas, embeddings=embs)