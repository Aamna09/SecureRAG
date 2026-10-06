# SecureRAG – Secure Enterprise RAG Application

It is a lightweight enterprise RAG application designed to provide grounded responses from a policy knowledge base while incorporating security and access-control checks.

## Overview

The application combines semantic retrieval with security controls to reduce the risk of unauthorized, irrelevant, or unsafe responses. Users submit questions through a FastAPI endpoint, and the system validates the request, applies authorization and security checks, retrieves relevant policy content, and returns a grounded response with source attribution.

## Key Features

- **Semantic Retrieval:** Uses Sentence Transformers (`all-MiniLM-L6-v2`) to generate embeddings and retrieve relevant policy content using cosine similarity.
- **Role-Based Authorization:** Restricts access to policy information based on the user's assigned role.
- **PII Detection:** Identifies potentially sensitive information in user queries before processing.
- **Prompt-Injection Detection:** Checks incoming queries for common prompt-injection patterns.
- **Confidence Thresholding:** Uses retrieval similarity scores to determine whether sufficient relevant context is available.
- **Grounded Responses:** Returns responses based on retrieved policy content with source attribution.
- **FastAPI Backend:** Provides an API endpoint for submitting and processing user questions.

## Architecture

```text
User Query
    ↓
Query Validation
    ↓
PII Detection
    ↓
Prompt-Injection Check
    ↓
Role-Based Authorization
    ↓
Semantic Retrieval
    ↓
Confidence Threshold
    ↓
Grounded Policy Response
    ↓
Source Attribution
```

## Technology Stack

- Python
- FastAPI
- Sentence Transformers
- JSON
- Uvicorn

## How It Works

1. A user submits a question through the FastAPI `/ask` endpoint.
2. The system checks the query for PII and potential prompt-injection attempts.
3. The user's role is validated against the requested policy information.
4. The query is converted into an embedding using Sentence Transformers.
5. The system compares the query embedding with policy embeddings using cosine similarity.
6. Retrieved content is evaluated against a confidence threshold.
7. If sufficient relevant context is found, the system returns a grounded response and identifies the source policy.
8. Requests that fail security, authorization, or confidence checks are rejected or returned with an appropriate response.

## Project Goals

This project demonstrates how RAG-based applications can incorporate security controls throughout the retrieval workflow rather than treating security as a separate layer. It focuses on grounded retrieval, access control, and common security risks associated with AI applications.

## Running Locally

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd SecureRAG
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the API

```bash
uvicorn app:app --reload
```

The API will be available locally at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Example Use Cases

SecureRAG can be used to demonstrate secure retrieval for enterprise policy questions such as:

- Employee access and permissions
- Security policies
- Data handling requirements
- Role-specific procedures
- Compliance-related questions

## Disclaimer

This project is a personal prototype created for demonstrating RAG architecture and AI application security concepts. It is not intended for production use without additional security, testing, monitoring, and infrastructure controls.
