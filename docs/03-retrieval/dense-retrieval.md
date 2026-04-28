# Dense Retrieval: Semantic Search with Embeddings

**Dense retrieval** uses embeddings to find documents with similar meaning to the query.

You've already learned the foundations:
- Embeddings convert text → vectors
- Cosine similarity measures vector similarity
- HNSW indexes find similar vectors quickly

This page applies those concepts to retrieval.

## How Dense Retrieval Works

```
User Query: "What is the status of my order?"
    ↓
[Embedding Model: Sentence-BERT]
    ↓
Query Embedding: [0.12, -0.45, 0.73, ..., 0.02]
    ↓
[Vector Database Index: HNSW]
    ↓
Step 1: Find 1000 similar vectors
Step 2: Compute exact cosine similarity to top 1000
Step 3: Return top-10 results
    ↓
Top Results:
1. "Your order #2401 will arrive Tuesday" (0.87 similarity)
2. "Track your order status here" (0.85 similarity)
3. "This is a cat picture" (0.23 similarity)
```

## Pros of Dense Retrieval

✅ **Captures meaning**: "What is my order status?" matches documents about "tracking" and "shipment"  
✅ **Semantic understanding**: Finds documents with similar intent, not just keywords  
✅ **Cross-lingual**: Works across languages (for multilingual models)  
✅ **Flexible**: Works for open-ended questions

## Cons of Dense Retrieval

❌ **Terrible for exact matches**: Order #1766 ≈ Order #1767 in embedding space  
❌ **Ambiguous queries fail**: "Bank" matches both financial and river banks  
❌ **Limited context**: Embedding model has maximum input length (usually 512-2048 tokens)  
❌ **Requires training data**: Need domain-specific embedding model for best results

## Example: Simple Dense Retrieval

```python
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.paginar import cosine_similarity

# Step 1: Create embeddings for all documents
documents = [
    "Your order #1766 has been confirmed",
    "Your order #1767 is being processed",
    "Your order #1765 will arrive tomorrow",
    "Here's a recipe for cat food",
    "The bank is open 9am-5pm weekdays"
]

model = SentenceTransformer('all-MiniLM-L6-v2')
doc_embeddings = model.encode(documents)

# Step 2: Embed query
query = "What about order #1766"
query_embedding = model.encode(query)

# Step 3: Find similar documents
similarities = cosine_similarity([query_embedding], doc_embeddings)[0]
top_k = 3
top_indices = np.argsort(-similarities)[:top_k]

# Step 4: Return results
for i in top_indices:
    print(f"{documents[i]}: {similarities[i]:.3f}")
```

**Output**:
```
Your order #1766 has been confirmed: 0.892
Your order #1767 is being processed: 0.883
Your order #1765 will arrive tomorrow: 0.819
```

**Problem**: Orders #1767 and #1765 are returned with almost the same score as #1766!

## When to Use Dense Retrieval

**Good for**:
- Natural language questions
- Semantic matching
- When word choice varies widely

**Bad for**:
- Exact identifiers (order numbers, SKUs, IDs)
- Structured data lookup
- Ambiguous queries

## Dense Retrieval with Vector Database

In production, use a vector database:

```python
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

client = QdrantClient(":memory:")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create collection and add documents
documents = ["...", "..."]
embeddings = model.encode(documents)

client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# Add with IDs and metadata
for i, (doc, emb) in enumerate(zip(documents, embeddings)):
    client.upsert(
        collection_name="documents",
        points=[PointStruct(id=i, vector=emb, payload={"text": doc})]
    )

# Query
query_embedding = model.encode("What about order #1766")
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    limit=10
)

for result in results:
    print(f"{result.payload['text']}: {result.score:.3f}")
```

## Dense + Multiple Embeddings Strategy

Some systems use multiple embedding models for different aspects:

```
Document: "Order #1766 shipped via FedEx"

Embedding Model 1 (semantic): [...]  # General semantics
Embedding Model 2 (order-specific): [...]  # Trained on order docs
Embedding Model 3 (logistics): [...]  # Trained on shipping docs

Query: "Where's my package"
→ Search with Model 3 (logistics-optimized)
```

This is more complex but improves quality for specialized domains.

## Embedding Model Choice Matters

```python
from sentence_transformers import SentenceTransformer

models_to_try = [
    'all-MiniLM-L6-v2',  # General purpose
    'all-mpnet-base-v2',  # Slightly better quality
    'multi-qa-MiniLM-L6-cos-v1',  # Optimized for Q&A
    'BAAI/bge-small-en-v1.5',  # New, good quality
]

query = "What's my order status?"

for model_name in models_to_try:
    model = SentenceTransformer(model_name)
    query_emb = model.encode(query)
    
    # The embeddings will be different!
    # Some models optimize better for Q&A
```

## Reranking Results

Dense retrieval alone might return 100 documents with similar scores. **Reranking** uses a more powerful (but slower) model to rank them:

```
Dense Retrieval (fast, finds 100 candidates):
├─ Document A: 0.87
├─ Document B: 0.85
├─ Document C: 0.84
└─ ... 97 more

Cross-Encoder Reranking (slow, ranks top 10):
1. Document A: 0.95  (was top 1)
2. Document C: 0.92  (was #3)
3. Document B: 0.88  (was #2)
```

Cross-encoders often reorder results with higher precision.

## Summary

| Aspect | Dense Retrieval |
|--------|-----------------|
| **What** | Embedding-based semantic search |
| **Similarity** | Cosine similarity between vectors |
| **Speed** | ⚡ Fast (HNSW indexing) |
| **Strength** | Captures meaning & synonyms |
| **Weakness** | Treats similar IDs as equivalent |
| **Best for** | Natural language questions |

## Key Limitation for This Tutorial

**Dense retrieval alone cannot solve the Order #1766 problem.**

You need additional strategies:
- [Hybrid Search](hybrid-search.md) — Combine with sparse/keyword
- [Metadata Filtering](metadata-filtering.md) — Filter by exact ID
- [Chunking Strategies](../04-exact-match/chunking-strategies.md) — Preserve IDs in text

## Next Steps

→ [Sparse Retrieval: BM25](sparse-retrieval.md) — Learn how keyword search finds exact matches

→ [Hybrid Search](hybrid-search.md) — The solution combining both
