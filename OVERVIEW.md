# Biometric Fraud Detection System

This document provides a comprehensive overview of the Biometric Fraud Detection application, its architecture, components, tools, and banking use cases.

## 🔧 Technologies and Tools Used

- **Python 3.11+**: Core language for backend and biometric processing.
- **FastAPI**: Web framework providing REST API endpoints for enrollment, scoring, and explanation.
- **ChromaDB**: Vector database for storing biometric baseline profiles and knowledge base documents used in RAG.
- **Anthropic Claude** *(optional)*: Large language model used to generate natural language explanations when RAG is enabled.
- **Clustering/Similarity libraries**: Python packages for vector math (e.g., NumPy, scikit-learn, or built-in vector operations).
- **Docker**: Containerization for deployment (Dockerfile included).

## 🧩 Application Components

1. **API Layer (`app/main.py`)**
   - Defines endpoints:
     - `/enroll` – accepts behavioral biometrics for a user and stores a baseline vector.
     - `/score` – calculates similarity between incoming transaction behavior and stored baseline.
     - `/explain` – triggers RAG process to produce a human-readable fraud explanation.

2. **Biometric Engine (`app/biometric.py`)**
   - Normalizes and vectorizes raw behavioral data (keystrokes, mouse, etc.).
   - Computes cosine similarity for scoring.

3. **Database Interface (`app/db.py`)**
   - Wraps ChromaDB operations: adding vectors, querying, and managing collections.
   - `query_chroma.py` is a utility for running SQL against the Chroma SQLite backend.

4. **Configuration (`app/config.py`)**
   - Holds environment-specific settings like database paths, thresholds, and API keys.

5. **RAG Knowledge Base (`app/rag_kb.py` and related storage)**
   - Loads fraud policy or KB documents into Chroma.
   - Used by the explanation endpoint to retrieve context for Claude.

6. **LLM Wrapper (`app/llm.py`)**
   - Interfaces with Anthropic Claude API when generating explanations.

7. **Application Entry Point (`app/main.py`)**
   - Starts FastAPI, wires up routes, and handles request validation.
   - May include startup tasks (e.g., initializing Chroma DB or loading embeddings).

## 📈 Workflow and Outputs

1. **Enrollment Flow**
   - Client sends user behavior metrics.
   - System computes vector and stores it.
   - Output: confirmation message and stored ID.

2. **Scoring Flow**
   - Client submits new transaction behavioral data.
   - System vectorizes and retrieves corresponding baseline.
   - Calculates cosine similarity and maps to risk level:
     - `High`, `Medium`, `Low`.
   - Output: JSON with score and risk category.

3. **Explanation Flow (RAG)**
   - Risky transaction triggers retrieval of relevant docs from KB.
   - Context passed to Claude to generate an audit explanation.
   - Output: human-readable explanation string.

## 🏦 Banking Use Cases

- **Real-time transaction monitoring**: Evaluate legitimacy of logins, transfers, or high-value purchases.
- **Secondary authentication**: Layer biometric scoring on top of passwords or OTPs.
- **Fraud investigation and reporting**: Provide explainable AI output to compliance teams.
- **Loss prevention**: Block or flag anomalous device/behavior patterns before funds are moved.

### Integration Points

- Banks can deploy the FastAPI service within their infrastructure or through container orchestration (e.g., Kubernetes).
- API endpoints easily called from existing backend systems or middleware.
- Thresholds and behavior feature sets may be tuned per customer or product.

## ✅ Key Benefits

- Non-intrusive, continuous authentication using behavioral biometrics.
- Explainability via RAG and LLMs to satisfy regulators.
- Scalable storage and retrieval of high-dimensional vectors with ChromaDB.
- Modular design allows switching LLMs or vector stores.

## 📦 Example Requests & Testing

Below are sample HTTP calls you can use to exercise the service. Modify `BASE_URL` to point at your running FastAPI instance (default `http://localhost:8000`).

### Enrollment
```bash
curl -X POST $BASE_URL/enroll \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user123","keystrokes":[0.11,0.09,0.12],"mouse_speed":1.5}'
```

### Scoring
```bash
curl -X POST $BASE_URL/score \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user123","keystrokes":[0.10,0.10,0.11],"mouse_speed":1.4}'
```

Response:
```json
{
  "similarity":0.935,
  "risk":"low"
}
```

### Explanation (RAG)
```bash
curl -X POST $BASE_URL/explain \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user123","transaction_id":"txn789","details":{...}}'
```

The JSON reply will include a human-readable explanation from the LLM.

POST /enroll

{
  "user_id": "u123",
  "avg_key_dwell_ms": 110,
  "avg_key_flight_ms": 85,
  "typing_error_rate": 0.02,
  "mouse_avg_speed": 1.3,
  "mouse_pause_rate": 0.18
}
POST /score

{
  "user_id": "u123",
  "transaction_id": "tx001",
  "amount": 240.5,
  "merchant": "AMAZON",
  "avg_key_dwell_ms": 112,
  "avg_key_flight_ms": 88,
  "typing_error_rate": 0.03,
  "mouse_avg_speed": 1.25,
  "mouse_pause_rate": 0.20
}

> **Tip:** You can also script tests in Python using `requests` or the FastAPI test client (`from fastapi.testclient import TestClient`).

## 🎤 Interview Talking Points

When discussing this project with an interviewer, emphasize:

1. **Motivation & Domain** – designed for financial institutions to detect fraud using behavioral biometrics, addressing limitations of static credentials.
2. **Architecture** – lightweight FastAPI backend, ChromaDB as a vector store, and optional RAG/LLM component for explainability.
3. **Technical Depth** – describe how raw biometrics are normalized, vectorized, and compared using cosine similarity. Mention threshold tuning and risk categorization.
4. **Scalability** – modular design lets you swap ChromaDB for another vector database or change the LLM provider. Discuss containerization with Docker.
5. **Security & Compliance** – handling of sensitive biometric data, reasoning about GDPR/PCI, and storing minimal personal information.
6. **Testing Strategy** – unit tests for vector math, integration tests hitting the API, and manual curl examples. Talk about how you could simulate different risk levels.
7. **RAG Explanation** – highlight how storing policy docs in the vector store and retrieving them improves auditability, and how Claude generates natural language explanations that meet compliance needs.
8. **Use Cases** – real-time transaction monitoring, secondary authentication, fraud investigations, and loss prevention.

### Optional Demo Plan

- Spin up API with `uvicorn app.main:app --reload`.
- Enroll a test user, score a mock transaction, then request an explanation.
- Show database contents by inspecting `chroma_store/chroma.sqlite3` or using `query_chroma.py`.
- If RAG is configured, load a few KB docs and show Claude’s output.

## ❗ Notes & Conversion to PDF

- Privacy: behavioral data should be handled according to regulations (e.g., GDPR).
- Security: secrets (API keys, DB passwords) managed outside code.
- The RAG component is optional; system works without LLM explanation.

### Generating a PDF

To create a PDF from this document:

```bash
pandoc OVERVIEW.md -o OVERVIEW.pdf
```

Or use any Markdown‑to‑PDF converter (VS Code extension, online tool, etc.).

---

This enriched overview can serve as the content for an interview handout or internal documentation.

---

This overview should help stakeholders and developers understand the application purpose, architecture, and how it may be utilized by financial institutions for fraud detection with behavioral biometrics.