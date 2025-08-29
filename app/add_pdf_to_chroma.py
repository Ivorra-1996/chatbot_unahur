import chromadb
from ollama import Ollama
import os

client = chromadb.Client()
collection = client.create_collection("pdf_collection")
ollama_client = Ollama()

def add_pdf_to_chroma(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    # Fragmentar texto por párrafos
    paragraphs = text.split("\n\n")
    for idx, para in enumerate(paragraphs):
        embedding = ollama_client.embed(para)
        collection.add(
            ids=[f"{os.path.basename(file_path)}_{idx}"],
            embeddings=[embedding.tolist()],
            metadatas=[{"source": file_path}],
            documents=[para]
        )

# Agregar PDF de prueba
add_pdf_to_chroma("data/unahur_info.txt")
print("Documento agregado a Chroma.")
