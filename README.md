# Precifica - MVP de Precificação para Padarias

Este é um MVP de um assistente de precificação para padarias, desenvolvido com Streamlit, OpenAI GPT-4 e Weaviate Cloud para RAG (Retrieval-Augmented Generation).

## Funcionalidades
- Interface de chat conversacional
- Respostas baseadas em produtos e preços da base de dados
- Busca semântica usando embeddings
- Deploy em nuvem com Railway

## Tecnologias
- **Frontend**: Streamlit
- **IA**: OpenAI GPT-4
- **Base de Dados Vetorial**: Weaviate Cloud
- **Deploy**: Railway

## Como Rodar Localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/yurileveinovacao/precifica.git
   cd precifica
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente:
   - `OPENAI_API_KEY`: Sua chave da API do OpenAI
   - `WEAVIATE_URL`: URL do seu cluster Weaviate Cloud (ex: https://seu-cluster.weaviate.cloud)
   - `WEAVIATE_API_KEY`: Chave da API do Weaviate Cloud

4. Execute o app:
   ```bash
   streamlit run app.py
   ```

## Deploy no Railway

1. Conecte o repositório ao Railway.
2. Configure as variáveis de ambiente no painel do Railway:
   - `OPENAI_API_KEY`
   - `WEAVIATE_URL`
   - `WEAVIATE_API_KEY`
3. Railway fará o deploy automaticamente.

## Estrutura do Projeto
- `app.py`: Aplicação principal Streamlit
- `setup_weaviate.py`: Script para configurar e popular o Weaviate
- `requirements.txt`: Dependências Python
- `lista.xlsx`: Base de dados de produtos (exemplo)

## Como Usar
- Digite perguntas sobre produtos e preços no chat.
- O assistente buscará produtos similares e gerará respostas com GPT-4.
