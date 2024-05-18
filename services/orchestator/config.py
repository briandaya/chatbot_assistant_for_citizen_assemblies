# Configuration for the LLM Ollama model
LLM_BASE_URL = '***REMOVED***'
LLM_MODEL_NAME = 'llama3'
LLM_KEEP_ALIVE = 0
LLM_REQUEST_TIMEOUT = 60
LLM_TEMPERATURE = 0.5 # 0.75

# Configuration for text embedding inference
EMBED_BASE_URL = "***REMOVED***"
EMBED_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
EMBED_TIMEOUT = 60
EMBED_BATCH_SIZE = 10

# Configuration for chunks (only for non-markdown documents)
CHUNK_SIZE = 1024
CHUNK_OVERLAP = 20

# Configuration for Weaviate
WEAVIATE_URL = 'http://weviate:8080/'
WEAVIATE_HOST = 'weaviate'
WEAVIATE_PORT = 8080

# Collection name in Weaviate
INDEX_NAME = "Documents_md3"