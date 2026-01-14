from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS



class VectorStoreManager:
    def __init__(self):
        """
        Initializes text splitter and embedding model.
        """

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            add_start_index=True,
        )

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def create_vectorstore(self, docs):
        """
        Splits documents into chunks and creates FAISS vector store.
        """
        chunks = self.text_splitter.split_documents(docs)
        vector_store = FAISS.from_documents(chunks, self.embedding_model)
        return vector_store

    def save_vectorstore(self, vector_store, path: str):
        """
        Saves FAISS vector store to disk.
        """
        vector_store.save_local(path)

    @staticmethod  # Use staticmethod or self depending on design choice
    def load_vectorstore(path: str):
        """
        Loads FAISS vector store from disk.
        """
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        return FAISS.load_local(
            path,
            embeddings,
            allow_dangerous_deserialization=True
        )

