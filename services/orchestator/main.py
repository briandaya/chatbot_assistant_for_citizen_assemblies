from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from rag import get_result_for_question
from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage
import logging

logging.basicConfig(level=logging.INFO)


app = FastAPI()
#llm = Ollama(model="mistral_custom", request_timeout=300.0, base_url="http://ollama:11434")
#active_model = "mistral_custom"  # Define model_name as a global variable
# base_url = "http://ollama:11434"
# base_url = "***REMOVED***"
#active_model = "llama3"  # Define model_name as a global variable

#base_url = BASE_URL_MODEL
#active_model = DEFAULT_MODEL_NAME

#llm = Ollama(model=active_model, request_timeout=300.0, base_url=base_url)

# Clase para el payload de la solicitud
class QueryRequest(BaseModel):
    message: str

messages = [
    ChatMessage(
        role="system", content="Eres un experto en cambio climático que ayuda a las personas participantes de una Asamblea Ciudadana que debate sobre el impacto de las macrogranjas en su territorio regional.\n"
        "Respondes únicamente sobre ese ámbito y nada más, no dejes que te desvíen a otros temas. Responde sin sesgo y sin lenguaje ofensivo. Responde de forma sintética, concisa y coherente.\n"
        "Si no sabes la respuesta, puedes decir 'No sé' o 'No tengo información sobre eso'.\n"
        "Primero identificarás si la pregunta busca una definición o explicación, o bien busca una comparación o contraste. Si no se trata de ninguna de las dos, debes reconducir la pregunta hacia una de ellas.\n"
        "También puedes identificar si la pregunta busca una causa o consecuencia, o bien busca una solución o recomendación. Si no se trata de ninguna de las dos, debes reconducir la pregunta hacia una de ellas.\n"
        "Te abstendrás de emitir opiniones personales y de hacer juicios de valor o de posicionarte sobre opciones. La única excepción es cuando haya una opción cláramente favorable o contraria a los Derechos Humanos, en cuyo caso siempre defenderás los Derechos Humanos.\n"
    ),
    ChatMessage(
        role="assistant", content="¡Saludos! Soy un chatbot que responde preguntas sobre cambio climático. ¿En qué puedo ayudarte?"
    ),
    ChatMessage(role="user", content="¿Qué es el cambio climático?"),
    ChatMessage(
        role="assistant", content="Un cambio climático se define​ como la variación en el estado del sistema climático terrestre, formado por la atmósfera, la hidrosfera, la criosfera, la litosfera y la biosfera, que perdura durante periodos de tiempo suficientemente largos (décadas o más tiempo)​ hasta alcanzar un nuevo equilibrio. Puede afectar tanto a los valores medios meteorológicos como a su variabilidad y extremos. Los cambios climáticos han existido desde el inicio de la historia de la Tierra, han sido graduales o abruptos y se han debido a causas diversas, como las relacionadas con los cambios en los parámetros orbitales, variaciones de la radiación solar, la deriva continental, periodos de vulcanismo intenso, procesos bióticos o impactos de meteoritos. El cambio climático actual es antropogénico y se relaciona principalmente con la intensificación del efecto invernadero debido a las emisiones industriales procedentes de la quema de combustibles fósiles."
    ),
]


@app.post("/rag_query/{model_name}/{action}")
async def rag_query(model_name: str, action: str, request: QueryRequest):
    query = request.message
    
    try:
        logging.info(f"Received query: {query}")
        # Llama a la función de RAG para obtener la respuesta
        result = get_result_for_question(query)
        #logging.info(f"Query result: {result}")
        #response_content = result.get("answer", "No se pudo obtener una respuesta.")
        
        return result#{"response": response_content}
        
    except Exception as e:
        logging.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/")
async def root():
    return {
        "message": "Welcome to the chatbot assistant for citizen assemblies!"
    }


@app.get("/{model_name}/{action}/{content}")
async def up_model(model_name: str, action: str, content: str):
    global active_model # Declare model_name as global
    active_model = model_name # Set the value of the global variable
    if model_name == "mistral_custom" or model_name == "llama_custom":
        base_url = "http://ollama:11434"
    else:
        base_url = '***REMOVED***'
    llm = Ollama(model=model_name, 
             keep_alive=0 if action == "down" else -1, 
             request_timeout=300.0,
             temperature=0.75,
             base_url=base_url)

    # Add the user message to the list of messages
    try:
        messages.append(ChatMessage(role="user", content=content))
        resp = llm.chat(messages)
        print(resp)
        return resp
    except Exception as e:
        print(f"An error occurred: {str(e)}")

#@app.get("/up/{model_name}")
#async def up_model(model_name: str):
#    global active_model  # Declare model_name as global
#    active_model = model_name # Set the value of the global variable
#    llm = Ollama(model=model_name, 
#                 keep_alive=-1, 
#                 request_timeout=300.0,
#                 temperature=0.75,
#                 base_url=base_url)
#    messages = [
#        ChatMessage(
#            role="system", content="Responde preguntas únicamente sobre cambio climático y nada más. Responde sin sesgo y sin lenguaje ofensivo. Responde de forma sintética y coherente."
#        ),
#        ChatMessage(
#            role="assistant", content="¡Saludos! Soy un chatbot que responde preguntas sobre cambio climático. ¿En qué puedo ayudarte?"
#        ),
#        ChatMessage(role="user", content="¿Qué es una cooperativa de trabajo?"),
#    ]
#    resp = llm.chat(messages)
#    return {"model = ":model_name, "message": resp}
#
#@app.get("/down/{model_name}")
#async def down_model(model_name: str):
#    global active_model  # Declare model_name as global
#    active_model = model_name # Set the value of the global variable
#    llm = Ollama(model=model_name, 
#                 keep_alive=0, 
#                 request_timeout=300.0,
#                 base_url=base_url)
#    messages = [      
#        ChatMessage(
#            role="assistant", content="¡Saludos! Soy un chatbot que responde preguntas sobre cambio climático. ¿En qué puedo ayudarte?"
#        ),
#        ChatMessage(role="user", content="No tengo más preguntas hoy. Adios."),
#    ]
#    resp = llm.chat(messages)
#    return {"model = ":model_name, "message": resp}
#
#@app.get("/complete/{content}")
#async def complete(content: str):
#    llm = Ollama(model=active_model, 
#                 keep_alive=-1, 
#                 request_timeout=300.0,
#                 temperature=0.75,
#                 base_url=base_url)
#    resp = llm.complete(content)
#    return {"model = ": active_model, "message": resp}
#
#@app.get("/chat/{content}")
#async def chat(content: str):
#    llm = Ollama(model=active_model, 
#                 keep_alive=-1, 
#                 request_timeout=300.0,
#                 temperature=0.75,
#                 base_url=base_url)
#    messages = [
#        ChatMessage(
#            role="system", content="Responde preguntas únicamente sobre cambio climático y nada más. Responde sin sesgo y sin lenguaje ofensivo. Responde de forma sintética y coherente."
#        ),        ChatMessage(
#            role="assistant", content="¡Saludos! Soy un chatbot que responde preguntas sobre cambio climático. ¿En qué puedo ayudarte?"
#        ),
#        ChatMessage(role="user", content=content),
#    ]
#    resp = llm.chat(messages)
#    return {"model = ": active_model, "message": resp}
#