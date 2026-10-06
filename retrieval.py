import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def load_policies():
    with open("data/policies.json", "r") as file:
        return json.load(file)


def create_embeddings(texts):
    return model.encode(texts)


def retrieve_policies(query, policies, top_k=3):
    # Create text for each policy
    policy_texts = [
        policy["title"] + " " + policy["content"]
        for policy in policies
    ]

    # Convert query and policies into embeddings
    query_embedding = create_embeddings([query])
    policy_embeddings = create_embeddings(policy_texts)

    # Calculate similarity between query and each policy
    similarities = cosine_similarity(
        query_embedding,
        policy_embeddings
    )[0]

    results = []

    for policy, score in zip(policies, similarities):
        results.append({
            "title": policy["title"],
            "content": policy["content"],
            "score": float(score)
        })

    # Highest similarity first
    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_k]
