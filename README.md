# 🛡️ Biometric Fraud Detection with RAG + Chroma + Claude

A financial-grade fraud detection system that combines:

- **Behavioral Biometrics**
- **Vector Database (ChromaDB)**
- **RAG (Retrieval Augmented Generation)**
- **Anthropic Claude (LLM)**
- **FastAPI backend**

This system detects fraudulent transactions by comparing real-time behavioral biometric signals against a stored baseline profile.

---

# 🧠 Architecture Overview

## System Components

1. **FastAPI Application**
   - REST API for enroll, score, and explain

2. **ChromaDB (Vector Database)**
   - Stores biometric baseline vectors
   - Stores fraud knowledge base documents (RAG)

3. **Biometric Engine**
   - Converts user behavior into numeric vectors
   - Performs similarity scoring

4. **Anthropic Claude (Optional RAG)**
   - Generates audit-friendly fraud explanations

---

# 🔍 How Fraud Detection Works

## Step 1 — Enrollment
User baseline behavioral biometrics are stored:
- Keystroke dynamics
- Mouse movement patterns
- Error rates
- Speed metrics

These are normalized and stored as vectors in ChromaDB.

---

## Step 2 — Scoring a Transaction
When a new transaction occurs:

1. Convert behavioral signals → vector
2. Retrieve baseline vectors from Chroma
3. Compute cosine similarity
4. Assign risk level:

| Similarity | Risk |
|------------|------|
| ≥ 0.92     | Low  |
| 0.85–0.91  | Medium |
| < 0.85     | High |

Lower similarity → Higher fraud risk.

---

## Step 3 — RAG Explanation (Optional)
If enabled:

1. Retrieve relevant fraud policy documents from Chroma
2. Send context + transaction data to Claude
3. Generate human-readable audit explanation

---

# 📂 Project Structure
