import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_store")
KB_DIR = os.getenv("KB_DIR", "./data/kb_docs")