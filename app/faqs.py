from db import SessionLocal, FAQ
from embeddings import collection, embed_text
import numpy as np

def search_faq(user_question, top_k=1):
    # 1️⃣ Primero buscar coincidencia exacta en SQL
    session = SessionLocal()
    faq = session.query(FAQ).filter(FAQ.pregunta.ilike(f"%{user_question}%")).first()
    if faq:
        session.close()
        return faq.respuesta

    # 2️⃣ Si no hay match exacto, buscar semánticamente en Chroma
    embedding = embed_text(user_question).tolist()
    results = collection.query(query_embeddings=[embedding], n_results=top_k)
    session.close()

    if results and len(results['metadatas'][0]) > 0:
        return results['metadatas'][0][0]['respuesta']
    else:
        return "No tengo información suficiente."