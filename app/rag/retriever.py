import numpy as np
from app.rag.embeddings import embed_texts
from app.core.config import TOP_K

# Queries like "list all your certifications" need every matching document,
# not the top-k most similar ones. Semantic ranking cannot answer them.
ENUMERATION_WORDS = ("list", "all", "every", "what are", "name all", "how many")


class Retriever:
    def __init__(self, store):
        self.store = store

    def _infer_filters(self, query: str) -> dict:
        q = query.lower()

        if "policy" in q or "cdc" in q or "public health" in q:
            return {"project_name": "rag_policy_navigator"}

        if "rag" in q or "retrieval augmented generation" in q:
            return {"system": "Retrieval Augmented Generation"}

        if "lms" in q or "learning management" in q:
            return {"system": "Learning Management System"}

        if "cert" in q or "aws" in q:
            return {"source": "certification"}

        if "databricks" in q or "lakehouse" in q:
            return {"system": "databricks"}

        return {}

    def _infer_enumeration(self, query: str) -> str | None:
        """Return the source to enumerate in full, or None for normal retrieval."""
        q = query.lower()

        if not any(w in q for w in ENUMERATION_WORDS):
            return None

        if "cert" in q:
            return "certification"

        if "project" in q or "built" in q or "build" in q:
            return "project"

        return None

    def _enumerate(self, source: str):
        """Return every chunk for a source, so nothing is silently dropped."""
        items = [
            {"text": text, "metadata": meta}
            for text, meta in zip(self.store.texts, self.store.metadata)
            if meta.get("source") == source
        ]

        # For projects, one chunk per file is enough to name and summarise them
        # all; sending all 13 chunks would blow the context for no extra value.
        if source == "project":
            items = [i for i in items if i["metadata"].get("chunk_id") == 0]

        return sorted(
            items,
            key=lambda i: (i["metadata"].get("file", ""), i["metadata"].get("chunk_id", 0)),
        )

    def retrieve(self, query: str):
        source = self._infer_enumeration(query)
        if source:
            results = self._enumerate(source)
            if results:
                return results

        q_emb = embed_texts([query])[0]
        q_emb = np.array([q_emb]).astype("float32")

        filters = self._infer_filters(query)

        # Search wide enough that filtering cannot starve the result set: a
        # narrow candidate window used to return fewer than TOP_K matches.
        candidates = self.store.index.ntotal if filters else TOP_K * 2
        candidates = min(candidates, self.store.index.ntotal)

        scores, idxs = self.store.index.search(q_emb, candidates)

        results = []
        for i in idxs[0]:
            if i < 0:
                continue

            meta = self.store.metadata[i]
            # Apply metadata filtering
            if filters:
                if not all(meta.get(k) == v for k, v in filters.items()):
                    continue

            results.append({
                "text": self.store.texts[i],
                "metadata": meta
            })

            if len(results) == TOP_K:
                break

        return results
