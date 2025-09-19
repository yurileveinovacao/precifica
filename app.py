import streamlit as st
import weaviate
import pandas as pd
from openai import OpenAI
from weaviate.classes.config import Property, DataType
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar OpenAI
client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Conectar ao Weaviate Cloud
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=os.getenv("WEAVIATE_URL"),
    auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WEAVIATE_API_KEY"))
)

# Função para obter embedding
def get_embedding(text):
    response = client_openai.embeddings.create(input=text, model="text-embedding-ada-002")
    return response.data[0].embedding

# Função para buscar produtos similares
def search_products(query, limit=5):
    logger.info(f"Buscando produtos para query: {query}")
    collection = client.collections.get("Produto")
    query_vector = get_embedding(query)
    response = collection.query.near_vector(
        near_vector=query_vector,
        limit=limit,
        return_properties=["produto", "valor_unitario", "fornecedor"]
    )
    products = response.objects
    logger.info(f"Encontrados {len(products)} produtos: {[p.properties['produto'] for p in products]}")
    return products

# Função para gerar resposta com GPT-4
def generate_response(query, products):
    context = "\n".join([
        f"Produto: {p.properties['produto']}, Valor: {p.properties['valor_unitario']}, Fornecedor: {p.properties['fornecedor']}"
        for p in products
    ])
    prompt = f"Baseado nos produtos abaixo, responda à pergunta do cliente sobre precificação:\n\nProdutos:\n{context}\n\nPergunta: {query}"
    logger.info(f"Gerando resposta para query: {query} com contexto: {context}")
    response = client_openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response.choices[0].message.content
    logger.info(f"Resposta gerada: {answer}")
    return answer

# Interface Streamlit
st.title("Precifica - Assistente de Precificação para Padarias")

# Inicializar histórico de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada para nova mensagem
if prompt := st.chat_input("Digite sua pergunta sobre produtos e preços..."):
    # Adicionar mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gerar resposta
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            products = search_products(prompt)
            if products:
                response = generate_response(prompt, products)
                st.markdown(response)
                # Adicionar produtos relacionados
                st.markdown("**Produtos relacionados:**")
                for p in products:
                    st.markdown(f"- {p.properties['produto']} (R$ {p.properties['valor_unitario']}) - {p.properties['fornecedor']}")
            else:
                response = "Nenhum produto encontrado relacionado à sua pergunta."
                st.markdown(response)
    
    # Adicionar resposta ao histórico
    st.session_state.messages.append({"role": "assistant", "content": response})
