import os
from app.rag.chunking import chunk_text

def infer_metadata(file_path: str) -> dict:
    file_name = os.path.basename(file_path)
    parent_dir = os.path.basename(os.path.dirname(file_path))

    metadata = {
        "file": file_name,
        "source": "general"
    }

    # Certifications
    if "certification" in file_name.lower():
        metadata.update({
            "source": "certification"
        })
    
    # Resume
    if "resume" in file_name.lower():
        metadata.update({
            "source": "resume"
        })

    # Projects folder
    if parent_dir == "projects":
        metadata.update({
            "source": "project",
            "project_name": file_name.replace(".md", "")
        })

    # LMS project
    if "lms" in file_name.lower():
        metadata.update({
            "domain": "backend",
            "system": "Learning Management System"
        })

    # RAG project
    if "rag" in file_name.lower():
        metadata.update({
            "domain": "generative_ai",
            "system": "Retrieval Augmented Generation"
        })

    return metadata

def load_documents(data_dir: str) -> list:
    docs = []

    for root, _, files in os.walk(data_dir):
        for file in files:
            if not file.endswith(".md"):
                continue

            path = os.path.join(root, file)

            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            chunks = chunk_text(text)
            base_metadata = infer_metadata(path)

            for idx, chunk in enumerate(chunks):
                docs.append({
                    "text": chunk,
                    "metadata": {
                        **base_metadata,
                        "chunk_id": idx
                    }
                })
    return docs
