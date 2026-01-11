from app.rag.embeddings import embed_texts
from app.rag.vectorstore import FAISSStore
from app.utils.loader import load_documents

DATA_DIR = "data"
INDEX_PATH = "index/faiss.index"
META_PATH = "index/metadata.pkl"
TEXT_PATH = "index/texts.pkl"

# Load docs
docs = load_documents(DATA_DIR)
texts = [d["text"] for d in docs]
metas = [d["metadata"] for d in docs]

# Embed
embeddings = embed_texts(texts)

# Build index
store = FAISSStore(dim=len(embeddings[0]))
store.add(embeddings, metas, texts)
store.save(INDEX_PATH, META_PATH, TEXT_PATH)

print("Index built successfully")