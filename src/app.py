import streamlit as st
from rag import RAGProcessor
from langchain_community.llms.ollama import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGSMITH_PROJECT_NAME", "chatbot-rag")
os.environ["LANGCHAIN_SESSION"] = os.getenv("LANGSMITH_SESSION_NAME", "SesionDePrueba")

st.set_page_config(page_title="Chatbot RAG", layout="centered")
st.title("🤖 Chatbot RAG con PDF + LangSmith")

uploaded_file = st.file_uploader("📄 Sube un archivo PDF", type="pdf")

if uploaded_file:
    with open("data/documento.pdf", "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ PDF cargado correctamente.")
    rag = RAGProcessor("data/documento.pdf")
    if st.button("🔍 Procesar y crear base de datos"):
        with st.spinner("Procesando documento y generando embeddings..."):
            docs = rag.load_and_split()
            rag.create_vector_store(docs)
            st.success("✅ Base de datos creada y persistida.")

if os.path.exists("chroma_db"):
    rag = RAGProcessor("data/documento.pdf")
    rag.load_vector_store()

    llm = Ollama(model="llama3", temperature=0.7)

    prompt_template = """
    Responde en español de forma clara, completa y profesional utilizando la siguiente información del documento:

    {context}

    Pregunta: {question}
    Respuesta:
    """
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=rag.vector_store.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

    st.markdown("### 💬 Haz una pregunta sobre el documento:")
    user_question = st.text_input("Pregunta:")

    if user_question:
        with st.spinner("Generando respuesta..."):
            result = qa_chain(user_question)
            st.markdown("### 🤖 Respuesta:")
            st.write(result["result"])

            with st.expander("📚 Fragmentos usados"):
                for i, doc in enumerate(result["source_documents"]):
                    st.markdown(f"**Fragmento {i+1}:**")
                    st.write(doc.page_content)
