from retrieval import load_policies, retrieve_policies


def generate_answer(query, results):
    if not results or results[0]["score"] < 0.35:
        return "I don't have enough information in the knowledge base to answer that."

    best_policy = results[0]

    return best_policy["content"]


policies = load_policies()

query = "My credit card disappeared. What should I do?"

results = retrieve_policies(query, policies)

print("Retrieved policies:")

for result in results:
    print(
        result["title"],
        "->",
        round(result["score"], 3)
    )

print("\nAnswer:")
print(generate_answer(query, results))
