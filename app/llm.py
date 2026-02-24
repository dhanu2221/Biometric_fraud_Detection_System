import os
from anthropic import Anthropic


client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def explain_with_claude(*, user_id: str, tx: dict, kb_snippets: list[dict]) -> str:
    context = "\n\n".join(
        f"[{s['source']}]\n{s['text'][:1200]}" for s in kb_snippets
    )

    prompt = f"""
You are a fraud risk analyst assistant for a financial institution.
Write a concise, audit-friendly explanation.

User: {user_id}
Transaction: {tx}

Reference materials (internal playbooks/policies):
{context}

Requirements:
- Explain why the transaction was scored that way.
- Mention biometric similarity score and what it implies.
- Suggest next action (allow / step-up auth / hold for review).
- Keep it factual, no speculation.
"""

    msg = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=350,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text