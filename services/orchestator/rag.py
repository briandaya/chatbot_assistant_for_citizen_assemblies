from config import *
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.embeddings.text_embeddings_inference import TextEmbeddingsInference
from llama_index.core import VectorStoreIndex, Settings
import weaviate
import os
import logging


logging.basicConfig(level=logging.INFO)


# Function to set up the embeddings model
def setup_embedding_model():
    return TextEmbeddingsInference(
        model_name=EMBED_MODEL_NAME,
        base_url=EMBED_BASE_URL,
        timeout=EMBED_TIMEOUT, 
        embed_batch_size=EMBED_BATCH_SIZE
    )

# Function to set up the LLM model
def setup_llm_model():
    return Ollama(
        model=LLM_MODEL_NAME, 
        keep_alive=LLM_KEEP_ALIVE, 
        request_timeout=LLM_REQUEST_TIMEOUT, 
        temperature=LLM_TEMPERATURE, 
        base_url=LLM_BASE_URL
    )

# Function to configure settings for LLM and embedding model
def configure_settings(llm_model, embed_model):
    Settings.llm = llm_model
    Settings.embed_model = embed_model

# Function to initialize the query engine
def initialize_query_engine(weaviate_client, index_name, text_key="content"):
    vector_store = WeaviateVectorStore(weaviate_client=weaviate_client, 
                                       index_name=index_name,
                                       text_key=text_key)
    index = VectorStoreIndex.from_vector_store(vector_store)
    return index.as_query_engine(similarity_top_k=5)

# Main function to get the result for a given question
def get_result_for_question(question):
    # Initialize models and settings
    embed_model = setup_embedding_model()
    llm_model = setup_llm_model()
    configure_settings(llm_model, embed_model)

    # Connect to Weaviate
    WEAVIATE_URL = os.getenv('WEAVIATE_URL', 'http://weaviate:8080/')
    logging.info(f"Iniciando la conexión a weaviate: {WEAVIATE_URL}")
    weaviate_client = weaviate.connect_to_local(host=WEAVIATE_HOST, port=WEAVIATE_PORT)
    logging.info(f"Conectado a weaviate")

    # Initialize query engine
    query_engine = initialize_query_engine(weaviate_client, INDEX_NAME)

    # Query the engine
    result = query_engine.query(question)
    result_md = result.response
    logging.info(f"result.response: {result_md}")
    
    sources = "Fuentes: \n"
    unique_file_names = set(info['file_name'] for info in result.metadata.values())
    for name in unique_file_names:
        sources += f"- {name}\n"
    
    logging.info(f"sources: {sources}")
    result_md = result_md + sources


    # Close Weaviate client
    weaviate_client.close()
    
    return result

