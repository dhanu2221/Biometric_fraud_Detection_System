from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import numpy as np

from app.db import get_or_create_collection

app = FastAPI(title="Biometric Fraud")

profiles = get_or_create_collection("biometric_profiles")

class EnrollRequest(BaseModel):
    user_id: str
    avg_key_dwell_ms: float
    avg_key_flight_ms: float
    typing_error_rate: float
    mouse_avg_speed: float
    mouse_pause_rate: float

def to_vec(req: EnrollRequest):
    v = np.array([
        req.avg_key_dwell_ms,
        req.avg_key_flight_ms,
        req.typing_error_rate,
        req.mouse_avg_speed,
        req.mouse_pause_rate
    ], dtype=np.float32)
    # simple normalization (placeholder)
    return ((v - v.mean()) / (v.std() + 1e-8)).tolist()

@app.post("/enroll")
def enroll(req: EnrollRequest):
    vec = to_vec(req)
    sid = str(uuid.uuid4())

    profiles.add(
        ids=[sid],
        embeddings=[vec],
        metadatas=[{"user_id": req.user_id, "type": "baseline"}],
        documents=[f"baseline session for user {req.user_id}"]
    )
    return {"status": "ok", "session_id": sid}

class ScoreRequest(EnrollRequest):
    transaction_id: str
    amount: float
    merchant: str

@app.post("/score")
def score(req: ScoreRequest):
    qvec = to_vec(req)

    res = profiles.query(
        query_embeddings=[qvec],
        n_results=5,
        where={"user_id": req.user_id},
        include=["embeddings"]
    )

    candidates = res.get("embeddings")
    if candidates is None:
        candidates = []
    else:
        candidates = list(candidates[0])  # list of embedding vectors

    if len(candidates) == 0:
        return {
            "transaction_id": req.transaction_id,
            "risk": "unknown",
            "biometric_similarity": None
        }

    q = np.array(qvec, dtype=np.float32)
    sims = []
    for emb in candidates:
        b = np.array(emb, dtype=np.float32)
        sim = float(np.dot(q, b) / (np.linalg.norm(q) * np.linalg.norm(b) + 1e-8))
        sims.append(sim)

    best = max(sims)

    if best >= 0.92:
        risk = "low"
    elif best >= 0.85:
        risk = "medium"
    else:
        risk = "high"

    return {
        "transaction_id": req.transaction_id,
        "risk": risk,
        "biometric_similarity": best,
        "amount": req.amount,
        "merchant": req.merchant
    }

@app.get("/")
def root():
    return {"status": "ok", "service": "biometric-fraud-rag"}