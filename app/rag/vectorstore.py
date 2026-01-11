import faiss
import numpy as np
import pickle

class FAISSStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatIP(dim)
        self.metadata = []
        self.texts = []

    def add(self, embeddings, metadatas, texts):
        self.index.add(np.array(embeddings).astype("float32"))
        self.metadata.extend(metadatas)
        self.texts.extend(texts)

    def save(self, index_path, meta_path, text_path):
        faiss.write_index(self.index, index_path)
        with open(meta_path, "wb") as f:
            pickle.dump(self.metadata, f)
        
        with open(text_path, "wb") as f:
            pickle.dump(self.texts, f)

    def load(self, index_path, meta_path, text_path):
        self.index = faiss.read_index(index_path)
        with open(meta_path, "rb") as f:
            self.metadata = pickle.load(f)
        
        with open(text_path, "rb") as f:
            self.texts = pickle.load(f)