# Development of Reliable Conversational Agents for Citizen Assemblies

Prototype for Final Degree Project in Applied Data Science

Brianda Yáñez-Arrondo 2024

[![en](https://img.shields.io/badge/lang-en-blue.svg)](https://github.com/briandaya/chatbot_assistant_for_citizen_assemblies/blob/master/README.md)
[![es](https://img.shields.io/badge/lang-es-red.svg)](https://github.com/briandaya/chatbot_assistant_for_citizen_assemblies/blob/master/README.es.md)


The main goal of this project is to develop a reliable conversational assistant prototype based on Large Language Models (LLMs) to support citizen participation in deliberative assemblies. The assistant aims to facilitate access to specialized information, assist in informed deliberation, and promote equity in democratic participation.

The project emphasizes the use of open-source technologies such as Docker, Weaviate, LlamaIndex, and Streamlit, as well as compact, open models like Llama3 and Qwen2.

## Structure

- **services/**: Contains key services such as the orchestrator, Streamlit, and Weaviate.
- **docker-compose-watch.yml**: Configuration for deploying services with Docker.
- **ingestion/**: Scripts and notebooks for document ingestion.

## Advanced Project

This prototype is a preliminary version. The improved version is available in [this repository](https://github.com/briandaya/dev_chatbot_assistant_for_citizen_assemblies.git).

For more technical details and the full project description, see the [Final Degree Project Report](https://drive.google.com/file/d/15chRPKXqdmKBtf4jqpUAn-FyHuK9HTDL/view?usp=drive_link).

## Usage

1. Clone the repository.
2. Customize the model access settings.
3. Start the services with Docker Compose: `docker-compose -f docker-compose-watch.yml up`.
