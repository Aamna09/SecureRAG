from fastapi import FastAPI
from pydantic import BaseModel
import re

from retrieval import load_policies, retrieve_policies

app = FastAPI(title="SecureSupport AI")

policies = load_policies()


class QueryRequest(BaseModel):
    question: str
    role: str = "customer"


def is_prompt_injection(question):
    suspicious_patterns = [
        "ignore previous instructions",
        "ignore all instructions",
        "disregard previous instructions",
        "reveal your system prompt",
        "show me your system prompt",
        "bypass security",
        "bypass the rules"
    ]

    question_lower = question.lower()

    return any(
        pattern in question_lower
        for pattern in suspicious_patterns
    )


def contains_pii(question):
    patterns = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "card_number": r"\b(?:\d[ -]*?){13,16}\b"
    }

    for pii_type, pattern in patterns.items():
        if re.search(pattern, question):
            return pii_type

    return None


def authorize_policies(role):
    return [
        policy
        for policy in policies
        if policy.get("access") == role
    ]


def generate_answer(question, results):
    if not results or results[0]["score"] < 0.35:
        return "I don't have enough information in the knowledge base to answer that."

    return results[0]["content"]


@app.post("/ask")
def ask_question(request: QueryRequest):

    if is_prompt_injection(request.question):
        return {
            "question": request.question,
            "answer": "I can't process requests that attempt to bypass system instructions.",
            "source": None,
            "confidence": 0
        }

    pii_type = contains_pii(request.question)

    if pii_type:
        return {
            "question": "[REDACTED]",
            "answer": "Please do not include sensitive personal information in your question.",
            "source": None,
            "confidence": 0,
            "security_flag": pii_type
        }

    authorized_policies = authorize_policies(request.role)

    if not authorized_policies:
        return {
            "question": request.question,
            "answer": "You are not authorized to access this information.",
            "source": None,
            "confidence": 0,
            "security_flag": "unauthorized_role"
        }

    results = retrieve_policies(
        request.question,
        authorized_policies
    )

    answer = generate_answer(
        request.question,
        results
    )

    return {
        "question": request.question,
        "answer": answer,
        "source": results[0]["title"] if results else None,
        "confidence": round(results[0]["score"], 3) if results else 0
    }
