import streamlit as st
from api_client import query_backend
 
st.set_page_config(
    page_title="NeoHorse-1 Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

 
st.markdown("""
    <style>
    /* Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        color: #f8fafc;
    }
    
    /* Headers Styling */
    .main-header {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .sub-header {
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    /* Source Badges */
    .source-badge {
        display: inline-block;
        background: rgba(99, 102, 241, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(129, 140, 248, 0.3);
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-right: 6px;
        margin-top: 8px;
    }

    /* Buttons Style */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1, #a855f7);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px 0 rgba(168, 85, 247, 0.39);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(168, 85, 247, 0.55);
    }
    </style>
""", unsafe_allow_html=True)
 
with st.sidebar:
    st.image("https://img.icons8.com/isometric-folders/512/brain.png", width=80)
    st.title("🤖 System Console")
    st.markdown("---")
    
    st.markdown("**Core Architecture:**")
    st.caption("• **Vector DB:** FAISS")
    st.caption("• **LLM:** Groq Llama-3.1")
    st.caption("• **Embeddings:** MiniLM-L6-v2")
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_query = None
        st.rerun()

 
st.markdown('<div class="main-header">NeoHorse-1 Knowledge Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Ask technical questions regarding document specs, functions, and evaluation metrics.</div>', unsafe_allow_html=True)
 
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello Eng. Zainab! I am your RAG Knowledge Assistant. How can I help you analyze the technical report today?", "sources": []}
    ]

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None
 
st.markdown("##### 💡 Suggested Sample Queries:")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📌 What is NeoHorse-1?", use_container_width=True):
        st.session_state.pending_query = "What is NeoHorse-1 and what is its main purpose?"

with col2:
    if st.button("🏗️ System Architecture?", use_container_width=True):
        st.session_state.pending_query = "Can you summarize the core architectural modules of the project?"

with col3:
    if st.button("🛠️ Tech Stack Info?", use_container_width=True):
        st.session_state.pending_query = "List the main tech stack dependencies used in this system."

st.markdown("---")
 
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("sources"):
            st.markdown("**Retrieved Sources:**")
            sources_html = "".join([f'<span class="source-badge">📄 {src}</span>' for src in msg["sources"]])
            st.markdown(sources_html, unsafe_allow_html=True)

 
user_query = st.chat_input("Type your technical query here...")
 
if st.session_state.pending_query:
    user_query = st.session_state.pending_query
    st.session_state.pending_query = None
 
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query, "sources": []})
    with st.chat_message("user"):
        st.write(user_query)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching vector index and generating answer..."):
            res = query_backend(user_query)
            answer = res.get("answer", "No answer generated.")
            sources = res.get("sources", [])

            st.write(answer)
            if sources:
                st.markdown("**Retrieved Sources:**")
                sources_html = "".join([f'<span class="source-badge">📄 {src}</span>' for src in sources])
                st.markdown(sources_html, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
    st.rerun()