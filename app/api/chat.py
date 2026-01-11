from fastapi import APIRouter, Request, HTTPException
from openai import OpenAI
from collections import defaultdict
from time import time

from app.rag.retriever import Retriever
from app.rag.vectorstore import FAISSStore
from app.core.prompts import SYSTEM_PROMPT
from app.utils.openai import call_openai
from app.models.chat import ChatRequest, ChatResponse

router = APIRouter()
client = OpenAI()

REQUESTS = defaultdict(list)
WINDOW = 60
LIMIT = 30

store = FAISSStore(dim=1536)
store.load("index/faiss.index", "index/metadata.pkl", "index/texts.pkl")
retriever = Retriever(store)

chat_cache: dict[str, str] = {}

ALLOWED_KEYWORDS = {
    "project", "experience", "certification", "aws",
    "lms", "rag", "policy", "navigator", "resume", "skills",
    "education", "degree", "background", "work", "history",
    "chatbot", "anuj", "maharjan", "technical", "proficiencies",
    "portfolio"
}

def is_about_me(query: str) -> bool:
    q = query.lower()
    return any(k in q for k in ALLOWED_KEYWORDS)

@router.post("/chat", response_model=ChatResponse)
def chat(request: Request, req: ChatRequest):
    ip = request.client.host
    now = time()
    REQUESTS[ip] = [t for t in REQUESTS[ip] if now - t < WINDOW]
    if len(REQUESTS[ip]) >= LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests")
    REQUESTS[ip].append(now)

    query = req.query.strip()

    if not query:
        return {"answer": "Please ask a valid question."}  
    
    normalized_query = query.lower()

    if normalized_query in chat_cache:
        return {"answer": chat_cache[normalized_query]}

    if not is_about_me(normalized_query):
        return {
            "answer": "I can only answer questions about my background, projects, and experience"
        }

    contexts = retriever.retrieve(query)
    if not contexts:
        return {
            "answer": "I don't have information about that."
        }
    
    MAX_CHUNKS = 3
    MAX_CHARS = 800

    context_text = "\n".join([c["text"][:MAX_CHARS] for c in contexts[:MAX_CHUNKS]])

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {query}"}
    ]
    answer = call_openai(client, messages)
    # answer = "Test answer"

    chat_cache[normalized_query] = answer

    return {"answer": answer}