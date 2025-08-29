import chromadb
from chromadb.utils import embedding_functions
from ollama import Ollama

client = chromadb.Client()
collection = client.get_collection("pdf_collection")
ollama_client = Ollama()

def answer_question_from_pdfs(user_question, top_k=3):
    # Generar embedding de la pregunta
    question_embedding = ollama_client.embed(user_question)

    # Buscar los fragmentos más cercanos en Chroma
    results = collection.query(query_embeddings=[question_embedding.tolist()], n_results=top_k)

    # Combinar fragmentos y armar prompt estricto
    context = "\n\n".join(results['documents'][0])
    prompt = f"""
    Usá SOLO la información del siguiente contexto para responder.
    No inventes nada. Si no hay información suficiente, decí "No tengo información suficiente".

    Contexto:
    {context}

    Pregunta: {user_question}
    """

    response = ollama_client.generate(prompt)
    return response