import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "enterprise-qa-secret-key-2024")

    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASEDIR, "instance", "db_enterprise_qa.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-key-2024")
    JWT_ACCESS_TOKEN_EXPIRES = 86400

    OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    LLM_MODEL = os.environ.get("LLM_MODEL", "qwen3.5-4b:latest")
    EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "nomic-embed-text")

    CHROMA_PERSIST_DIR = os.path.join(BASEDIR, "db_enterprise_qa_chroma")
    CHROMA_COLLECTION_NAME = "enterprise_qa_docs"

    UPLOAD_FOLDER = os.path.join(BASEDIR, "uploads")
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"txt", "pdf", "docx", "md"}

    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50