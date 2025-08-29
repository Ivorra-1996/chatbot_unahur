import chromadb
from chromadb.utils import embedding_functions
import numpy as np

# Conectar Chroma
client = chromadb.Client()
collection = client.create_collection("faqs_collection")

# Ejemplo: generar embeddings con Ollama local
from ollama import Ollama

ollama_client = Ollama()

def embed_text(text):
    # Usando Ollama para embeddings
    embedding = ollama_client.embed(text)
    return np.array(embedding)

def add_faq_to_chroma(faq_id, pregunta, respuesta):
    embedding = embed_text(pregunta)
    collection.add(
        ids=[str(faq_id)],
        embeddings=[embedding.tolist()],
        metadatas=[{"respuesta": respuesta}],
        documents=[pregunta]
    )