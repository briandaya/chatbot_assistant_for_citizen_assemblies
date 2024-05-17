import streamlit as st
import requests
import json
import os
import time
import uuid
import gc

# Page configuration and literal strings
st.set_page_config(
    page_title="Prototipo de Asistente Conversacional Responsable para Asambleas Ciudadanas",
    page_icon="🪆",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'About': "Prototipo de Asistente Conversacional Responsable para Asambleas Ciudadanas.\n\nDesarrollado por [Brianda Yáñez Arrondo](https://www.linkedin.com/in/briandayanez/) \n\nEn colaboración con [Deliverativa.org](https://Deliberativa.org/) \n\nTrabajo de Fin de Grado de [Ciencia de Datos Aplicada (Applied Data Science)](https://www.uoc.edu/es/estudios/grados/grado-data-science) en la Universitat Oberta de Catalunya (UOC). \n\nLicencia GNU - [Repositorio en Gitlab](about:blank)",
    }
)

st.title("Prototipo de Asistente Conversacional Responsable para Asambleas Ciudadanas")
hide_footer_style = """
    <style>
    .reportview-container .main footer {visibility: hidden;}    
    """
st.markdown("##### Bienvenida!. Para comenzar, selecciona un modelo de lenguaje y escribe tu pregunta en el cuadro de chat.")# URL del servicio orquestador
#st.markdown("<style>.st-emotion-cache-ul70r3 p {font-size: 0.85rem; font-weight: 200;} .st-emotion-cache-ul70r3 p:nth-child(1),p:nth-child(2) {font-size: 1rem; font-weight: bold;} .st-emotion-cache-ul70r3 p:last-child {display: none;}", unsafe_allow_html=True)


# URL of the orchestrator service
ORCHESTRATOR_URL = "http://orchestator:8000"

# Load model options
model_options = json.loads(os.getenv('AVAILABLE_MODELS', '[]'))
model_names = [option['MODEL_LABEL'] for option in model_options]
model_name_to_key = {option['MODEL_LABEL']: option['MODEL_NAME'] for option in model_options}

# Initialize session state variables
if "selected_model" not in st.session_state:
    st.session_state["selected_model"] = model_name_to_key[model_names[0]] if model_names else ""

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "query_engine" not in st.session_state:
    st.session_state["query_engine"] = None

if "context" not in st.session_state:
    st.session_state["context"] = None

if "id" not in st.session_state:
    st.session_state.id = uuid.uuid4()
    st.session_state.file_cache = {}

session_id = st.session_state.id
client = None

# Function to reset chat history
def reset_chat():
    st.session_state.messages = []
    st.session_state.context = None
    gc.collect()

# Function to send the user message to the orchestrator
def send_message(model_name, action, message):
    url = f"{ORCHESTRATOR_URL}/rag_query/{model_name}/{action}"
    print(f"Sending message to {url}")
    payload = {"message": message}
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        decoded_response = response.json()
        
        sources = "\n>Fuentes: \n"
        unique_file_names = set(info['file_name'] for info in decoded_response["metadata"].values() )
        for name in unique_file_names:
            sources += f">- {name}\n"

        return decoded_response.get("response", "No se ha recibido respuesta")+sources+json.dumps(decoded_response["metadata"], indent=4)
    except requests.exceptions.RequestException as e:
        error_message = f"Error al comunicarse con el orquestador: {e}"
        st.error(error_message)
        return ""

# Clear chat history button
with st.sidebar:
    st.button("Clear ↺", on_click=reset_chat)

# Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Model selection dropdown
selected_model_label = st.selectbox("Elige tu modelo", model_names, index=0)
st.session_state["selected_model"] = model_name_to_key[selected_model_label]

# Chat input box
if prompt := st.chat_input("Introduce tu pregunta:"):
    # Add user message to chat history
    st.session_state["messages"].append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        model_key = st.session_state["selected_model"]
        streaming_response = send_message(model_key, "chat", prompt)
        
        for chunk in streaming_response:
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state["messages"].append({"role": "assistant", "content": full_response})
