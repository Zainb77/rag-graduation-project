# 🤖 RAG-Powered Knowledge Application

An end-to-end Retrieval-Augmented Generation (RAG) system built with FastAPI, Streamlit, LangChain, FAISS, and Ollama.

## 📐 System Architecture

```text
+-------------------+       HTTP POST        +-------------------+
|                   |  ------------------->  |                   |
| Streamlit UI      |   /query {question}    |  FastAPI Backend  |
| (Frontend)        |                        | (RAG Pipeline)    |
|                   |  <-------------------  |                   |
+-------------------+     {answer, sources}  +---------+---------+
                                                       |
                                            +----------+----------+
                                            |                     |
                                            v                     v
                                    +---------------+     +---------------+
                                    |  FAISS Vector |     |  Ollama LLM   |
                                    |     Store     |     |  (Llama 3)    |
                                    +---------------+     +---------------+

## 🛠️ Tech Stack

* **Frontend:** Streamlit, Requests
* **Backend:** FastAPI, Pytest, Uvicorn
* **Vector Store:** FAISS
* **Embeddings:** HuggingFace `all-MiniLM-L6-v2`
* **LLM Orchestration:** Groq API (`llama-3.1-8b-instant`), LangChain

---

## 📁 Project Structure
rag-graduation-project/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   └── rag_engine.py
│   ├── tests/
│   │   └── test_query.py
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/
│   ├── app.py
│   ├── api_client.py
│   ├── .env.example
│   └── requirements.txt
│
├── notebooks/
│   └── rag_pipeline.ipynb
│
├── .env.example
├── .gitignore
└── README.md

---

## 🚀 Setup & Installation

### 1. Backend Setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

2. Frontend Setup
cd frontend
streamlit run app.py

3. Run Automated Tests
python -m pytest backend/tests/test_query.py

📡 API Endpoints
GET /health: Returns system operational status.

POST /query: Accepts JSON {"question": "..."} and returns answer with retrieved document citations.

---

## 🎥 Video Demonstration

Watch the full system walkthrough and live demo here:
👉 [Click to Watch Demo Video](https://drive.google.com/file/d/1NBeAWyHYkRcFoQOfb4yqRB74vWiUIEy5/view?usp=sharing)