from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
import os

class RAGProcessor:
    def __init__(self, pdf_path, persist_directory="chroma_db"):
        self.pdf_path = pdf_path
        self.persist_directory = persist_directory
        self.embedding_model = OllamaEmbeddings(model="nomic-embed-text")
        self.vector_store = None

    def load_and_split(self):
        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        split_docs = splitter.split_documents(documents)
        return split_docs

    def create_vector_store(self, documents):
        self.vector_store = Chroma.from_documents(
            documents, embedding=self.embedding_model, persist_directory=self.persist_directory
        )
        self.vector_store.persist()

    def load_vector_store(self):
        if os.path.exists(self.persist_directory):
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding_model
            )
        else:
            raise FileNotFoundError("La base de datos vectorial no existe. Primero crea el vector store.")

    def query(self, query_text, k=3):
        if not self.vector_store:
            self.load_vector_store()
        results = self.vector_store.similarity_search(query_text, k=k)
        return results
