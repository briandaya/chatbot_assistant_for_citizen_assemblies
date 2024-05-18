from config import *
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.embeddings.text_embeddings_inference import TextEmbeddingsInference
from llama_index.core import VectorStoreIndex, Settings, ChatPromptTemplate
from llama_index.core.llms import ChatMessage, MessageRole

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


    # Custom Text QA Prompt
    qa_prompt_str = (
        "La información de contexto está abajo.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Dada la información del contexto y no el conocimiento previo, "
        "responde la pregunta, en el mismo idioma: {query_str}\n"
    )
    
    basic_content = (
                "Eres un experto en cambio climático que ayuda a las personas participantes de una Asamblea Ciudadana "
                "que debate sobre el impacto de las macrogranjas en su territorio regional.\n"
                "Respondes únicamente sobre ese ámbito y nada más, no dejes que te desvíen a otros temas. "
                "Responde sin sesgo y sin lenguaje ofensivo. Responde de forma sintética, concisa y coherente.\n"
                "Si no sabes la respuesta, puedes decir 'No sé' o 'No tengo información sobre eso'.\n"
                "Primero identificarás si la pregunta busca una definición o explicación, o bien busca una comparación o contraste. "
                "Si no se trata de ninguna de las dos, debes reconducir la pregunta hacia una de ellas.\n"
                "También puedes identificar si la pregunta busca una causa o consecuencia, o bien busca una solución o recomendación. "
                "Si no se trata de ninguna de las dos, debes reconducir la pregunta hacia una de ellas.\n"
                "Te abstendrás de emitir opiniones personales y de hacer juicios de valor o de posicionarte sobre opciones.\n"
                "La única excepción es cuando haya una opción claramente favorable o contraria a los Derechos Humanos, en cuyo caso siempre defenderás los Derechos Humanos.\n"
                "Si te preguntan ventajas/inconvenientes, estructura la respuesta en una tabla con formato markdown, con una columna para las ventajas y otra para inconvenientes.\n"
                "Si te preguntan una comparativa, estructura la respuesta en una tabla con formato markdown, con una columna para cada elemento a comparar.\n"
                "No te posicionarás ni recomendarás una opción. Si la respuesta incluye la opinión de expertos deberás cítalos\n"
            )
    chat_text_qa_msgs = [
        ChatMessage(
            role=MessageRole.SYSTEM,
            content=basic_content,
        ),
        ChatMessage(role=MessageRole.USER, content=qa_prompt_str),
    ]
    text_qa_template = ChatPromptTemplate(chat_text_qa_msgs)

    # Custom Refine Prompt
    refine_prompt_str = (
        "Tenemos la oportunidad de refinar la respuesta original "
        "(solo si es necesario) con más contexto a continuación.\n"
        "------------\n"
        "{context_msg}\n"
        "------------\n"
        "Dado el nuevo contexto, refinar la respuesta original para mejorar "
        "responde a la pregunta, en el mismo idioma: {query_str}. "
        "Si el contexto no es útil, envíe la respuesta original de nuevo.\n"
        "Respuesta original: {existing_answer}"
    )
    
    chat_refine_msgs = [
        ChatMessage(
            role=MessageRole.SYSTEM,
            content=basic_content,
        ),
        ChatMessage(role=MessageRole.USER, content=refine_prompt_str),
    ]
    refine_template = ChatPromptTemplate(chat_refine_msgs)

    return index.as_query_engine(text_qa_template=text_qa_template,
                                 refine_template=refine_template,
                                 similarity_top_k=5)


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

