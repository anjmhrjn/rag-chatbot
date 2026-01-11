## AI-Powered Personal Portfolio Chatbot (RAG System)

### Objective

Build an AI assistant capable of answering questions **strictly about my background, skills, projects, and certifications** using grounded retrieval instead of hallucinated responses.

### System Architecture

* Retrieval-Augmented Generation (RAG) pipeline
* External knowledge base built from resume and project documentation

```
User Query → Embedding → Vector Search (FAISS) → Context Injection → LLM Response
```

### Key Features

* Token-based document chunking for accurate retrieval
* Vector search using **FAISS**
* Strict prompt grounding to prevent hallucinations
* Modular backend design for future extensions (re-ranking, memory)

### Technologies Used

* Backend: FastAPI
* Vector Store: FAISS
* Embeddings: OpenAI embeddings / sentence transformers
* LLMs: OpenAI models or local LLMs (configurable)

### Outcome

* Accurate, context-grounded responses to portfolio-related questions
* Improved recruiter engagement through interactive portfolio experience
* Designed as a production-ready system rather than a demo chatbot

---