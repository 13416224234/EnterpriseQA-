from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from config import Config
from services.embedding_service import EmbeddingService

class RAGService:
    def __init__(self):
        self.llm = Ollama(model=Config.LLM_MODEL, base_url=Config.OLLAMA_BASE_URL, temperature=0.3, top_p=0.85)
        self.embedding_service = EmbeddingService()
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""Answer the question based on the provided documents. Keep answers concise and factual.

Rules:
1. Use ONLY document content. Never fabricate.
2. If documents lack the answer, say "知识库中暂无相关信息"
3. Cite sources as [来源X]
4. Answer in the same language as the question
5. Use bullet points when listing multiple items

Documents:
{context}

Question: {question}

Answer:"""
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def ask(self, question, conversation_history=None):
        try:
            search_results = self.embedding_service.similarity_search(question, k=8)
            context_parts = []
            sources = []
            for i, result in enumerate(search_results):
                context_parts.append("[来源 %d] %s" % (i + 1, result["content"]))
                sources.append({
                    "document_title": result["metadata"].get("title", "Unknown"),
                    "content_preview": result["content"][:120] + "...",
                    "score": round(float(result["score"]), 4)
                })
            context = "\n\n".join(context_parts) if context_parts else "No relevant documents."
            if context_parts:
                response = self.chain.run(context=context, question=question)
            else:
                response = "知识库中暂无相关信息"
            return {"answer": response.strip(), "sources": sources, "has_context": len(context_parts) > 0}
        except Exception as e:
            return {"answer": "Error: %s" % str(e), "sources": [], "has_context": False}

rag_service = RAGService()