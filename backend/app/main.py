from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
 
 
from backend.app.rag_engine import RAGEngine
rag_system = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    rag_system["engine"] = RAGEngine()
    yield
    rag_system.clear()

app = FastAPI(title="RAG Application API", lifespan=lifespan)

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "RAG Backend Service Running"}

@app.post("/query", response_model=QueryResponse)
def handle_query(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    engine: RAGEngine = rag_system.get("engine")
    if not engine:
        raise HTTPException(status_code=500, detail="RAG Engine not initialized.")
    
    answer, sources = engine.ask(req.question)
    return QueryResponse(answer=answer, sources=sources)