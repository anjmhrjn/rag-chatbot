from openai import OpenAI
from app.core.config import OPENAI_API_KEY, EMBEDDING_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

def embed_texts(texts: list[str]):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )
    return [e.embedding for e in response.data]