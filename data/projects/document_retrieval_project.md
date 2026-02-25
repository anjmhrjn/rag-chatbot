# Document Retrieval System

## Overview

Document Retrieval is a full-stack intelligent document management and search platform designed to transform unstructured document collections into a searchable, structured knowledge base. The system addresses a core limitation of traditional keyword search — vocabulary mismatch — by combining semantic vector search with BM25 keyword matching through a hybrid retrieval strategy called Reciprocal Rank Fusion (RRF).

The platform supports multiple real-world domains including academic note retrieval, legal document management, and internal enterprise knowledge bases. Users can upload documents in multiple formats, and the system automatically extracts text, generates embeddings, and indexes content for fast and accurate natural language search.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Next.js Frontend                      │
│         Login · Register · Search · Upload · Documents       │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP (REST)
┌────────────────────────────▼────────────────────────────────┐
│                        FastAPI Backend                       │
│                                                             │
│   ┌─────────────┐   ┌──────────────┐   ┌────────────────┐  │
│   │ Auth Routes │   │ Ingest Routes│   │ Search Routes  │  │
│   │  JWT / bcrypt│   │ Parse·Chunk │   │ Hybrid RRF     │  │
│   └─────────────┘   │ Embed·Index  │   └───────┬────────┘  │
│                     └──────┬───────┘           │           │
└────────────────────────────┼───────────────────┼───────────┘
                             │                   │
              ┌──────────────┼───────────────────┼──────────┐
              │              │                   │          │
     ┌────────▼──────┐  ┌───▼──────┐    ┌───────▼──────┐   │
     │  PostgreSQL   │  │  Qdrant  │    │  BM25 Index  │   │
     │  Users        │  │  Vector  │    │  (in-memory) │   │
     │  Documents    │  │  Store   │    │              │   │
     │  Chunks       │  │          │    └──────────────┘   │
     └───────────────┘  └──────────┘                       │
              └──────────────────────────────────────────────┘
```

### Layers

**Ingestion Layer** — accepts uploaded files (PDF, DOCX, TXT, MD), extracts raw text using format-specific parsers, cleans and normalizes content, and splits it into overlapping chunks that preserve sentence boundaries.

**Processing Layer** — generates dense vector embeddings for each chunk using a local `sentence-transformers` model (`all-MiniLM-L6-v2`), requiring no external API calls. Embeddings are normalized for cosine similarity.

**Storage Layer** — chunks and their vectors are stored in Qdrant (vector database) for semantic retrieval. Chunk content and document metadata (owner, source, category, client, timestamp) are persisted in PostgreSQL. An in-memory BM25 index is rebuilt from PostgreSQL on every server startup.

**Retrieval Layer** — at query time, the system runs semantic search via Qdrant and keyword search via BM25 in parallel. Results are fused using Reciprocal Rank Fusion and filtered by a minimum relevance threshold before being returned to the user.

**Auth Layer** — JWT-based authentication with bcrypt password hashing. Every document and search operation is scoped to the authenticated user.

---

## Key Features

**Hybrid Search with Reciprocal Rank Fusion**
Pure semantic search can surface topically related but contextually irrelevant results. Pure keyword search fails when terminology differs. RRF combines ranked result lists from both strategies without requiring score normalization, producing more robust and precise retrieval than either approach alone.

**User-Scoped Document Isolation**
Every document is tied to the user who uploaded it via a foreign key. Qdrant queries are filtered by `uploaded_by` at the vector database level, and PostgreSQL queries include a user ID condition. No user can view, search, or delete another user's documents.

**Local Embedding Model**
Embeddings are generated using `sentence-transformers` running entirely on the host machine. There are no calls to external embedding APIs, which eliminates latency, cost, and data privacy concerns associated with sending document content to third-party services.

**Intelligent Text Chunking**
Documents are split into overlapping chunks using sentence-boundary-aware splitting. Overlap between chunks preserves context that would otherwise be lost at chunk boundaries, improving retrieval accuracy for queries that span multiple sentences.

**Relevance Thresholding**
A minimum cosine similarity threshold is applied at the Qdrant level, and a minimum RRF score threshold is applied after fusion. This prevents low-relevance chunks from appearing in results when a query has little to no overlap with the document corpus.

**Automatic BM25 Rebuild on Startup**
The BM25 index is an in-memory structure that does not persist across restarts. On startup, the system queries all chunk content from PostgreSQL and rebuilds the index automatically, ensuring keyword search is always consistent with the stored document corpus.

---

## Technologies Used

| Category | Technology | Purpose |
|---|---|---|
| Backend Framework | FastAPI | Async REST API, dependency injection, OpenAPI docs |
| Frontend Framework | Next.js 14 (App Router) | File-based routing, React server/client components |
| Styling | Tailwind CSS | Utility-first responsive UI |
| Vector Database | Qdrant | Semantic similarity search, metadata filtering |
| Relational Database | PostgreSQL | User accounts, document metadata, chunk content |
| ORM | SQLAlchemy (async) | Database models and async session management |
| Embeddings | sentence-transformers | Local dense vector generation (all-MiniLM-L6-v2) |
| Keyword Search | rank-bm25 | BM25Okapi in-memory keyword index |
| Authentication | python-jose + passlib | JWT token generation and bcrypt password hashing |
| Document Parsing | PyMuPDF, python-docx | PDF and DOCX text extraction |
| Containerization | Docker + Docker Compose | Multi-service orchestration and deployment |

---

## Outcomes

**Accurate cross-document retrieval** — Hybrid RRF search consistently surfaces the most relevant chunks even when the query uses different terminology than the source document, addressing the core vocabulary mismatch problem of keyword-only search.

**Noise reduction** — The dual threshold system (cosine similarity at the Qdrant level and RRF score at the fusion level) prevents unrelated documents from appearing in search results, which is particularly important in single-document or small-corpus scenarios.

**Complete user isolation** — Documents are scoped to individual users at both the database and vector search level, making the system suitable for multi-tenant deployments where data privacy between users is required.

**Zero external API dependencies for core functionality** — The embedding model runs locally, and all data remains within the self-hosted infrastructure. This makes the system viable for sensitive document domains such as legal and enterprise use cases where data cannot leave the organization's environment.