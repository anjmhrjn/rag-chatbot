## Agent-Orchestrated Adaptive RAG

### Objective

Move beyond flat single-index retrieval by building a multi-agent RAG system that understands query intent, routes to the right knowledge domain, and validates its own retrieval quality before generating an answer.

### Problem

Traditional RAG systems retrieve from one flat vector index regardless of what is being asked. Across complex, multi-domain technical knowledge bases this produces topically-adjacent but incorrect context, and there is no mechanism to detect when retrieved context is stale or insufficient — the model answers confidently either way.

### System Architecture

```
User Query
   ↓
Intent Classification Agent
   ↓
Routing → Domain-Specific Vector Namespace
   ↓
Retrieval
   ↓
Self-RAG Evaluation Loop (score relevance, flag stale context)
   ↓
Context Injection → LLM Response
```

### Key Features

* **Multi-agent LangChain orchestration** — specialized agents handle classification, routing, retrieval, and evaluation as distinct steps.
* **Intent-based namespace routing** — queries are directed to domain-specific vector namespaces instead of a single shared index, sharply improving answer precision.
* **Self-RAG evaluation loops** — retrieval quality is scored before generation, and stale or weak context is flagged rather than silently used.
* **Adaptive retrieval strategy** — the pipeline adjusts its retrieval path based on classified query intent rather than applying one fixed strategy to every question.

### Technologies Used

* Backend: Python
* Orchestration: LangChain (multi-agent)
* Vector Store: namespaced vector database
* Embeddings: Sentence Transformers / OpenAI embeddings
* LLMs: OpenAI models

### Outcome

* Improved answer precision across complex technical knowledge bases compared to flat single-index retrieval.
* Reduced manual review effort needed to trust output in production-facing AI workflows, by surfacing low-quality retrieval automatically.
* Demonstrated agentic RAG patterns — routing, self-evaluation, and adaptive retrieval — beyond basic document Q&A.

---
