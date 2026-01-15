from fastapi import Header, HTTPException
import os

EXPECTED_KEY = os.getenv("FRONTEND_SERVICE_KEY")

def verify_service_key(authorization: str = Header(None)):
    if EXPECTED_KEY is None:
        raise RuntimeError("FRONTEND_SERVICE_KEY not set")

    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
 
    if authorization != f"Bearer {EXPECTED_KEY}":
        raise HTTPException(status_code=401, detail="Invalid service key")
