# Policy Navigator — AI-Powered Public Health Policy Assistant

## Overview

**Policy Navigator** is a domain-specific AI assistant designed to support **public health policy analysis** using grounded, evidence-based responses. The system follows a **Retrieval-Augmented Generation (RAG)** architecture to ensure answers are derived strictly from authoritative policy documents rather than model assumptions.

The project was inspired by the **CDC Policy Analytical Framework** and focuses on structured reasoning for complex policy questions.

---

## Problem Statement

Public health policy analysis involves:

* Complex, multi-step reasoning
* Trade-offs across health outcomes, feasibility, and equity
* High risk if responses are hallucinated or ungrounded

Generic LLMs often produce confident but unsupported policy advice. This project addresses that risk by enforcing **context-grounded generation**.

---

## Solution

Built a **policy-restricted RAG system** that:

* Retrieves only from curated public health policy documents
* Structures responses using policy-analysis steps
* Refuses to answer when sufficient evidence is unavailable

The system is designed as a **decision-support assistant**, not a general chatbot.

---

## System Architecture

```
User Query
   ↓
Embedding
   ↓
Vector Search (FAISS)
   ↓
Context Filtering (Policy Documents Only)
   ↓
Context Injection
   ↓
LLM Response (Strict Grounding)
```

---

## Key Features

* **Advanced RAG pipeline** with strict context grounding
* **Metadata-based retrieval filtering** to restrict responses to policy sources
* **Explicit refusal behavior** when answers are not supported by retrieved context
* **Evaluation across multiple setups** (Vanilla LLM vs Basic RAG vs Advanced RAG)

---

## Evaluation Strategy

The system was evaluated using **10 complex public health policy questions**, each requiring:

* Problem framing
* Policy option analysis
* Consideration of implementation challenges

Results showed that:

* Vanilla LLM responses hallucinated policy steps
* Basic RAG improved factual grounding
* Advanced RAG with filtering produced the most reliable and structured answers

---

## Technologies Used

* Backend: Python
* Framework: LangChain-style RAG pipeline
* Vector Store: FAISS
* Embeddings: Sentence Transformers / OpenAI embeddings
* LLMs: OpenAI models

---

## Impact

* Demonstrated safe and reliable AI usage in **high-stakes policy domains**
* Showcased advanced RAG concepts beyond simple document Q&A
* Reinforced best practices for **hallucination prevention** in generative AI systems

---

## Recommended Metadata for Indexing

```json
{
  "source": "project",
  "project_name": "Policy Navigator",
  "domain": "public_policy",
  "framework": "CDC Policy Analytical Framework"
}
```
