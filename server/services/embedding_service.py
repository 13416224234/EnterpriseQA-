import os
import hashlib
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document as LangchainDocument
from config import Config

class EmbeddingService:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model=Config.EMBEDDING_MODEL,
            base_url=Config.OLLAMA_BASE_URL
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", "!", "?", " ", ""]
        )
        self.vector_store = Chroma(
            collection_name=Config.CHROMA_COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=Config.CHROMA_PERSIST_DIR
        )

    def split_and_vectorize(self, document_id, title, content):
        try:
            chunks = self.text_splitter.split_text(content)
            langchain_docs = []
            for idx, chunk_text in enumerate(chunks):
                chunk_id = hashlib.md5(f"{document_id}_{idx}_{chunk_text[:50]}".encode()).hexdigest()
                doc = LangchainDocument(
                    page_content=chunk_text,
                    metadata={"document_id": document_id, "chunk_index": idx, "title": title, "chunk_id": chunk_id}
                )
                langchain_docs.append(doc)
            if langchain_docs:
                self.vector_store.add_documents(langchain_docs)
            return True
        except Exception as e:
            print(f"Vectorization failed: {e}")
            return False

    def similarity_search(self, query, k=5, document_id=None):
        search_kwargs = {"k": k}
        if document_id:
            search_kwargs["filter"] = {"document_id": document_id}
        results = self.vector_store.similarity_search_with_score(query, **search_kwargs)
        formatted_results = []
        for doc, score in results:
            formatted_results.append({"content": doc.page_content, "score": float(score), "metadata": doc.metadata})
        return formatted_results

    def delete_document_vectors(self, document_id):
        try:
            results = self.vector_store.get(where={"document_id": document_id})
            if results and results.get("ids"):
                self.vector_store.delete(results["ids"])
            return True
        except Exception as e:
            print(f"Delete vectors failed: {e}")
            return False