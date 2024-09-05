# Projeto LLaMA AI com Spring e Python

Este projeto demonstra como integrar um modelo de linguagem LLaMA treinado com uma aplicação Spring Boot para criar um serviço de inferência. O treinamento do modelo é feito em Python, e o modelo treinado é acessado via uma API RESTful que o Spring utiliza para fornecer respostas.

## Índice

1. [Visão Geral](#visão-geral)
2. [Pré-requisitos](#pré-requisitos)
3. [Configuração do Ambiente](#configuração-do-ambiente)

## Visão Geral

Este projeto consiste em:

- Treinamento de um modelo de linguagem LLaMA usando Python.
- Criação de uma API RESTful com Flask para expor o modelo treinado.
- Integração com uma aplicação Spring Boot para fazer inferências através da API.


## Pré-requisitos

- Python 3.8 ou superior
- Java 17 ou superior
- Maven (para construir o projeto Spring)
- Pip (para gerenciar pacotes Python)

## Configuração do Ambiente

### Python

1. **Crie e ative um ambiente virtual**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows, use `venv\Scripts\activate`

2. Crie um arquivo requirements.txt com as seguintes dependências:
torch==2.0.0
transformers==4.34.0
flask==2.3.0
numpy==1.24.0
pandas==2.1.0
3. Instale as dependências:
pip install -r requirements.txt
