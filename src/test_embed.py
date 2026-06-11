from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [
    "How do I create a custom field in Twenty?",
    "Where can I find the data model settings?",
    "What is the weather like today?",  # unrelated, should score low
]

embeddings = model.encode(texts)

print(f"Model loaded. Each embedding has {embeddings.shape[1]} dimensions.\n")

# Compute cosine similarity between the first two (both CRM-related)
# and between first and third (unrelated) to sanity-check retrieval will work.
from sklearn.metrics.pairwise import cosine_similarity

sim_related = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
sim_unrelated = cosine_similarity([embeddings[0]], [embeddings[2]])[0][0]

print(f"Similarity: 'custom field' vs 'data model settings' = {sim_related:.3f}  (expect high)")
print(f"Similarity: 'custom field' vs 'weather today'       = {sim_unrelated:.3f}  (expect low)")
print("\nEmbedding model is working correctly." if sim_related > sim_unrelated else "\nUnexpected result — check model.")
