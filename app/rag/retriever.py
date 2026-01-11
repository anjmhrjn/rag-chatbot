import numpy as np
from app.rag.embeddings import embed_texts
from app.core.config import TOP_K


class Retriever:
    def __init__(self, store):
        self.store = store

    def _infer_filters(self, query: str) -> dict:
        q = query.lower()

        if "policy" in q or "cdc" in q or "public health" in q:
            return {"project_name": "Policy Navigator"}
        
        if "rag" in q or "Retrieval Augmented Generation" in q:
            return {"system": "Retrieval Augmented Generation"}

        if "lms" in q or "learning management" in q:
            return {"system": "Learning Management System"}

        if "certification" in q or "aws" in q:
            return {"source": "certification"}

        return {}

    def retrieve(self, query: str):
        q_emb = embed_texts([query])[0]
        q_emb = np.array([q_emb]).astype("float32")

        scores, idxs = self.store.index.search(q_emb, TOP_K * 2)

        filters = self._infer_filters(query)
        results = []

        for i in idxs[0]:
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
