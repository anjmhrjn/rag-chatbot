## Agent-Orchestrated Adaptive RAG

**Repository:** [github.com/anjmhrjn/agentic-rag](https://github.com/anjmhrjn/agentic-rag)

### Objective

Build a fully-local agentic RAG system that adapts its retrieval approach to each query, then measure empirically whether the added agentic machinery actually earns its cost.

### Problem

Standard RAG applies one fixed retrieval strategy to every question, regardless of whether the query is a simple lookup or a complex multi-part question. Agentic patterns such as query decomposition and self-reflection are widely assumed to fix this, but their benefits are rarely measured against the latency and complexity they introduce.

### System Architecture

An orchestrator routes each query across **five retrieval strategies**, coordinating specialized agents at each stage.

```
User Query
   ↓
Query Classifier Agent  (intent + complexity)
   ↓
Orchestrator → routes across five retrieval strategies
   ↓
Query Decomposer Agent  (multi-part queries)
   ↓
Retrieval + Answer Generation
   ↓
Answer Evaluator Agent
   ↓  (bounded two-retry reflection loop)
Final Answer
```

### Key Features

* **Orchestrated multi-strategy routing** — a single orchestrator selects among five retrieval strategies per query instead of applying one fixed pipeline to everything.
* **Specialized agent roles** — query-classifier, query-decomposer, and answer-evaluator agents each own one stage of the pipeline.
* **Bounded two-retry reflection loop** — the answer evaluator can trigger a retry, capped at two attempts so self-correction cannot loop indefinitely or run away with latency.
* **Fully local execution** — the entire pipeline runs on local models with no external API dependencies, keeping cost and data exposure at zero.
* **Dual-dataset ablation harness** — the system is instrumented to compare baseline, decomposition, and full-agentic configurations on the same queries.

### Evaluation

Ran a **dual-dataset ablation** across structured-retrieval and multi-hop question sets, isolating the contribution of each agentic component:

| Component | Structured retrieval | Multi-hop |
|---|---|---|
| Query decomposition (MRR) | **0.56 → 0.72** | collapses to **0.10** |
| Reflection loop | up to **6× latency**, no reliable quality gain | same |

### Technologies Used

* Backend: Python
* Architecture: multi-agent orchestration (classifier, decomposer, evaluator)
* Vector Store: local vector index
* Embeddings: local sentence embedding model
* LLM: locally-hosted model (no external API calls)

### Outcome

* Demonstrated that **query decomposition is workload-dependent, not universally beneficial** — it materially improves ranking on structured retrieval while actively degrading multi-hop performance.
* Showed that the **reflection loop was not worth its cost**, adding up to 6× latency without a reliable quality improvement.
* Produced a measured, evidence-backed view of agentic RAG rather than assuming the pattern helps — the kind of ablation that determines whether such a system should ship at all.

---
