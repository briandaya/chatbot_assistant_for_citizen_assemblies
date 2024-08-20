# Desarrollo de Agentes Conversacionales Confiables para Asambleas Ciudadanas.

Prototipo para TFG Grado de Ciencia de Datos Aplicada

Brianda Yáñez-Arrondo 2024

[![en](https://img.shields.io/badge/lang-en-blue.svg)](https://github.com/briandaya/chatbot_assistant_for_citizen_assemblies/blob/master/README.md)
[![es](https://img.shields.io/badge/lang-es-red.svg)](https://github.com/briandaya/chatbot_assistant_for_citizen_assemblies/blob/master/README.es.md)


El objetivo principal del proyecto es desarrollar un prototipo de asistente conversacional confiable basado en Modelos de Lenguaje de Gran Tamaño (LLMs) para apoyar la participación ciudadana en asambleas deliberativas. El asistente tiene como propósito facilitar el acceso a información especializada, ayudar en la deliberación informada y promover la equidad en la participación democrática.

Se destaca el uso de tecnologías de código abierto como Docker, Weaviate, LlamaIndex y Streamlit, así como modelos de lenguaje libres y compactos como Llama3 y Qwen2.

## Estructura

- **services/**: Contiene los servicios clave como el orquestador, Streamlit, y Weaviate.
- **docker-compose-watch.yml**: Configuración para desplegar los servicios con Docker.
- **ingestion/**: Scripts y notebooks para la ingesta de documentos.

## Proyecto Avanzado

Este prototipo es una versión preliminar. La versión mejorada está disponible en [este repositorio](https://github.com/briandaya/dev_chatbot_assistant_for_citizen_assemblies.git).

Para más detalles técnicos y la descripción completa del proyecto, consulta la [Memoria del TFG]([ruta/al/archivo.pdf](https://drive.google.com/file/d/15chRPKXqdmKBtf4jqpUAn-FyHuK9HTDL/view?usp=drive_link)).

## Uso

1. Clonar el repositorio.
2. Personalizar los accesos a los modelos.
3. Iniciar los servicios con Docker Compose: `docker-compose -f docker-compose-watch.yml up`.
