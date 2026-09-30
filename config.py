OLLAMA_URL = "http://localhost:11434/api/generate"

# CHANGE THIS if `ollama list` shows a different name
OLLAMA_MODEL = "qwen3:4b"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

TOP_K_VECTOR = 8
TOP_K_KEYWORD = 8
TOP_K_FINAL = 5

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

UPLOAD_DIR = "data/uploads"
VECTOR_DIR = "data/vectorstore"