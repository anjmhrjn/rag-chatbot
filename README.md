# Personal Portfolio RAG Chatbot

A production-style **Retrieval-Augmented Generation (RAG)** chatbot that answers questions strictly about my background, projects, and certifications. Built with **FastAPI**, **FAISS**, and LLMs, the system prioritizes grounded responses, low cost, and safety.

This project is designed to be used as an interactive assistant on my portfolio website.

---

## ✨ Key Features

* **Grounded answers only** – responses are generated strictly from retrieved context
* **Metadata-aware retrieval** – project-specific filtering (LMS, RAG, Policy Navigator, etc.)
* **Cost-aware design** – request gating, caching, and token caps
* **FastAPI backend** – clean API boundaries and schemas
* **FAISS vector store** – efficient semantic search
* **Production-minded guards** – refusal on out-of-scope queries

---

## 🧠 Architecture Overview

```
User Query
   ↓
Topic & Safety Gates
   ↓
Query Embedding
   ↓
FAISS Vector Search
   ↓
Metadata Filtering
   ↓
Context Injection
   ↓
LLM Response (Token-Capped)
```

If no relevant context is found, the system **does not call the LLM**.

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── api/
│   │   └── chat.py           # /chat endpoint
│   ├── models/
│   │   └── chat.py           # Pydantic request/response models
│   ├── rag/
│   │   ├── chunking.py       # Chunk documents
│   │   ├── embeddings.py     # Embedding logic
│   │   ├── retriever.py      # Retrieval + metadata filtering
│   │   └── vectorstore.py    # FAISS wrapper
│   ├── utils/
│   │   └── loader.py         # Document loading & chunking
│   │   └── openai.py         # openai api request
│   └── __init__.py
├── build_index.py            # Offline index builder
├── data/
│   ├── resume.md             # markdown of example document
├── index/
│   ├── faiss.index
│   ├── metadata.pkl
│   └── texts.pkl
└── README.md
```

---

## 🚀 Getting Started

### 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Build the FAISS index

```bash
python build_index.py
```

This step embeds documents and creates:

* `faiss.index`
* `metadata.pkl`
* `texts.pkl`

---

### 4. Run the API server

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 🧪 Example API Request

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain your Policy Navigator project"}'
```

### Example Response

```json
{
  "answer": "Policy Navigator is a project that ..."
}
```

---

## 🛡️ Safety & Cost Controls

* ❌ No LLM calls for out-of-scope questions
* ❌ No LLM calls when retrieval returns no context
* ✅ Output token cap (`max_tokens=200`)
* ✅ Context size limits (chunks + characters)
* ✅ In-memory caching for repeated queries
* ✅ Keyword-based topic gating

> The cheapest LLM request is the one you never make.

---

## 🔮 Planned Improvements

* Cross-encoder re-ranking
* Source citations per answer
* Redis-based caching
* Streaming responses

---

## 📄 License

MIT License

---
