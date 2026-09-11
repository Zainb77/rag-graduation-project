import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq

class RAGEngine:
    def __init__(self, index_path: str = None):
        # Initialize embedding model
        self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Set directory paths
        if index_path is None:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            index_path = os.path.join(BASE_DIR, "vectorstore", "faiss_index")

        # Load FAISS index
        if os.path.exists(index_path):
            self.vector_db = FAISS.load_local(
                index_path, 
                self.embedding_model, 
                allow_dangerous_deserialization=True
            )
            self.retriever = self.vector_db.as_retriever(search_kwargs={"k": 3})
            print(f"Vector store successfully loaded from: {index_path}")
        else:
            self.vector_db = None
            print(f"Vector store NOT found at: {index_path}")
        # Groq API configuration
        api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(
            model_name="openai/gpt-oss-120b",
            groq_api_key=api_key,
            temperature=0.2
        )

    def ask(self, question: str):
        if not self.vector_db:
            return "Vector store not initialized. Please run notebook first.", []
        
        try:
            docs = self.retriever.invoke(question)
            context = "\n\n".join([f"[Source Page {d.metadata.get('page', 0) + 1}]: {d.page_content}" for d in docs])
            
            prompt = f"""Answer the question based only on the context below. Include citations if applicable.

Context:
{context}

Question: {question}
Answer:"""

            response = self.llm.invoke(prompt)
            answer = response.content if hasattr(response, 'content') else str(response)
            
            sources = list(set([f"Page {d.metadata.get('page', 0) + 1}" for d in docs if hasattr(d, 'metadata')]))
            return answer, sources

        except Exception as e:
            print(f"Backend Exception: {e}")
            return f"Error processing request: {str(e)}", []