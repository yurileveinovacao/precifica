import weaviate
import pandas as pd
from openai import OpenAI
from weaviate.classes.config import Property, DataType
import os

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

# Deletar coleção se existir
try:
    client.collections.delete("Produto")
except:
    pass

# Criar coleção
collection = client.collections.create(
    name="Produto",
    properties=[
        Property(name="produto", data_type=DataType.TEXT),
        Property(name="valor_unitario", data_type=DataType.NUMBER),
        Property(name="fornecedor", data_type=DataType.TEXT),
    ]
)

# Ler dados
df = pd.read_excel('lista.xlsx')

# Inserir dados
with collection.batch.dynamic() as batch:
    for _, row in df.iterrows():
        vector = get_embedding(row['Produto'])
        batch.add_object(
            properties={
                "produto": row['Produto'],
                "valor_unitario": row['Valor unitário'],
                "fornecedor": row['Fornecedor']
            },
            vector=vector
        )

print("Dados inseridos com sucesso no Weaviate.")
