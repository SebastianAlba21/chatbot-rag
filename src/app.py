import streamlit as st
from src.rag import RAGProcessor
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

st.set_page_config(page_title="Chatbot RAG PDF", page_icon="🤖")

# Título
st.title("Chatbot interactivo con RAG y PDF")

# Subir PDF
uploaded_file = st.file_uploader("Carga tu archivo PDF", type=["pdf"])

if uploaded_file:
    with open("data/documento.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("PDF cargado correctamente")

    # Procesar PDF y crear o cargar vector store
    rag = RAGProcessor(pdf_path="data/documento.pdf")

    # Intentar cargar vector store, si no existe, crearla
    try:
        rag.load_vector_store()
        st.info("Base vectorial cargada desde disco")
    except FileNotFoundError:
        st.info("Creando base vectorial desde el PDF...")
        docs = rag.load_and_split()
        rag.create_vector_store(docs)
        st.success("Base vectorial creada y guardada")

    # Crear cadena RAG para responder preguntas
    retriever = rag.vector_store.as_retriever(search_kwargs={"k": 3})
    llm = Ollama(model="llama2")  # Ajusta el modelo a tu configuración Ollama local
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    # Historial de conversación
    if "history" not in st.session_state:
        st.session_state.history = []

    # Input para preguntas
    user_question = st.text_input("Haz tu pregunta sobre el PDF:")

    if user_question:
        with st.spinner("Buscando respuesta..."):
            answer = qa_chain.run(user_question)
            st.session_state.history.append({"Pregunta": user_question, "Respuesta": answer})

    # Mostrar historial
    if st.session_state.history:
        st.markdown("### Historial de conversación")
        for chat in st.session_state.history:
            st.markdown(f"**Pregunta:** {chat['Pregunta']}")
            st.markdown(f"**Respuesta:** {chat['Respuesta']}")
            st.markdown("---")
