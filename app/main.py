import streamlit as st
from faqs import search_faq
from rag import answer_question_from_pdfs

st.title("Chatbot UNAHUR")

user_question = st.text_input("Escribí tu pregunta:")

if st.button("Preguntar"):
    # Primero buscar en FAQs oficiales
    respuesta = search_faq(user_question)
    
    # Si no hay info suficiente, buscar en PDFs
    if respuesta == "No tengo información suficiente.":
        respuesta = answer_question_from_pdfs(user_question)
    
    st.write("💬 Respuesta:")
    st.write(respuesta)