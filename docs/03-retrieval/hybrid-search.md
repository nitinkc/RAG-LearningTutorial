# Hybrid Search: Combining Dense + Sparse

**Hybrid search** combines dense (semantic) and sparse (keyword) retrieval to get the best of both worlds.

This is the **solution to the Order #1766 problem** and the most effective retrieval strategy.

## The Hybrid Pipeline

```
User Query: "Order #1766"
    ├──────────────────────┬──────────────────────┐
    ↓                      ↓                      ↓
[Embed Query]      [Tokenize Query]      [Extract Filters]
    ↓                      ↓                      ↓
[Dense Search]      [BM25 Search]        [Metadata Filter]
    ↓                      ↓                      ↓
Dense Results:      Sparse Results:      Filtered Results:
├─ Order #1766: 0.98  ├─ Order #1766: 10.2  └─ Only ID="1766"
├─ Order #1767: 0.96  ├─ Order #1767: 2.1
└─ Order #1765: 0.95  └─ Order #1765: 1.9
    │                      │                      │
    └──────────────────────┴──────────────────────┘
                      ↓
            [Combine & Rank]
                      ↓
        1. Order #1766: 0.98 + 10.2 = 11.18 ✅
        2. Order #1767: 0.96 + 2.1 = 3.06
        3. Order #1765: 0.95 + 1.9 = 2.85
```

## Why Hybrid Works

| Problem | Dense Solution | Sparse Solution | Hybrid Solution |
|---------|---|---|---|
| "Order #1766" → returns #1767? | ❌ Yes (similar) | ✅ No (exact match) | ✅ Perfect |
| "What's my order status?" → finds right docs? | ✅ Yes | ❌ No (no keyword) | ✅ Perfect |
| Combines both strengths | N/A | N/A | ✅ Yes |

## Combining Scores: Three Approaches

### Approach 1: Simple Addition

```
hybrid_score = dense_score + sparse_score

Normalized:
hybrid_score = (dense_score - min) / (max - min) + (sparse_score - min) / (max - min)
```

**Pros**: Simple, equal weighting  
**Cons**: Scores have different ranges (need normalization)

```python
def hybrid_simple(dense_scores, sparse_scores):
    # Normalize to [0, 1]
    dense_norm = (dense_scores - dense_scores.min()) / (dense_scores.max() - dense_scores.min())
    sparse_norm = (sparse_scores - sparse_scores.min()) / (sparse_scores.max() - sparse_scores.min())
    
    # Combine
    hybrid = dense_norm + sparse_norm
    return hybrid

# Example
dense = np.array([0.98, 0.96, 0.95])
sparse = np.array([10.2, 2.1, 1.9])

hybrid = hybrid_simple(dense, sparse)
# Result: [1.98, 1.08, 1.00]
```

### Approach 2: Weighted Sum

```
hybrid_score = w_dense * dense_score + w_sparse * sparse_score

where w_dense + w_sparse = 1, typically 0.5 each
```

**Pros**: Tunable weights  
**Cons**: Need to find right weights (experiment)

<details>
<summary>View weighted combination code</summary>

```python
def hybrid_weighted(dense_scores, sparse_scores, w_dense=0.5, w_sparse=0.5):
    # Normalize
    dense_norm = (dense_scores - dense_scores.min()) / (dense_scores.max() - dense_scores.min())
    sparse_norm = (sparse_scores - sparse_scores.min()) / (sparse_scores.max() - sparse_scores.min())
    
    # Weighted combination
    hybrid = w_dense * dense_norm + w_sparse * sparse_norm
    return hybrid

# Try different weights
for w_dense in [0.3, 0.5, 0.7]:
    w_sparse = 1 - w_dense
    score = hybrid_weighted(dense, sparse, w_dense, w_sparse)
    print(f"Weights ({w_dense}, {w_sparse}): {score}")
```

</details>

### Approach 3: Reciprocal Rank Fusion (RRF)

Combine rankings, not raw scores:

```
RRF_score = 1/k + Σ 1 / (k + rank_i)

where k=60 (standard), rank_i is position (1-indexed)
```

**Pros**: Combines rankings directly (no normalization needed)  
**Cons**: Slightly more complex

<details>
<summary>View Reciprocal Rank Fusion code</summary>

```python
def reciprocal_rank_fusion(dense_indices, sparse_indices, k=60):
    """Combine based on ranking, not scores."""
    scores = {}
    
    # Add dense results
    for rank, doc_id in enumerate(dense_indices, 1):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    
    # Add sparse results
    for rank, doc_id in enumerate(sparse_indices, 1):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    
    # Sort by combined score
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

# Example
dense_ranking = [1, 2, 3]  # doc IDs in order of relevance
sparse_ranking = [1, 0, 2]

result = reciprocal_rank_fusion(dense_ranking, sparse_ranking)
print(result)  # [(1, score), (2, score), ...]
```

</details>

## Production Implementation

### Using Elasticsearch (Hybrid Query)

```python
from elasticsearch import Elasticsearch

es = Elasticsearch(['http://localhost:9200'])

query_text = "Order #1766"

# Hybrid query: BM25 + dense vectors
response = es.search(index="orders", body={
    "query": {
        "bool": {
            "should": [
                # Dense (vector) search
                {
                    "script_score": {
                        "query": {
                            "match_all": {}
                        },
                        "script": {
                            "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                            "params": {
                                "query_vector": query_embedding.tolist()
                            }
                        }
                    },
                    "boost": 1.0  # Equal weight
                },
                # Sparse (keyword) search
                {
                    "match": {
                        "text": {
                            "query": query_text,
                            "boost": 1.0
                        }
                    }
                }
            ]
        }
    },
    "size": 10
})
```

### Using Qdrant (Hybrid with Fusion)

```python
from qdrant_client import QdrantClient
from qdrant_client.models import SparseVector, PointStruct

client = QdrantClient(":memory:")

# Collection supports both dense and sparse
client.create_collection(
    collection_name="hybrid_orders",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    sparse_vectors_config={...}  # Also define sparse
)

# Add documents with both vectors
# ... (add points with both dense and sparse vectors)

# Hybrid search with fusion
results = client.search(
    collection_name="hybrid_orders",
    query_vector=query_dense_vector,
    sparse_query_vector=query_sparse_vector,
    fusion_func="rrf"  # Reciprocal Rank Fusion
)
```

### Using Pinecone (Hybrid Index)

```python
from pinecone import Pinecone

pc = Pinecone(api_key="...")
index = pc.Index("hybrid-index")

# Pinecone supports metadata filtering + dense vectors
# For hybrid, combine results from multiple queries:

# 1. Dense search
dense_results = index.query(
    vector=query_embedding,
    top_k=100,  # Retrieve more candidates
    include_metadata=True
)

# 2. Sparse search (using external BM25 index)
sparse_results = bm25_index.search(query_text, top_k=100)

# 3. Combine results (RRF or weighted)
combined = reciprocal_rank_fusion(
    [r.id for r in dense_results],
    [r.id for r in sparse_results]
)
```

## Complete Example: Building a Hybrid RAG System

```python
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import numpy as np

class HybridRetriever:
    def __init__(self, documents):
        self.documents = documents
        
        # Dense index
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = self.encoder.encode(documents)
        
        # Sparse index (BM25)
        corpus = [doc.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(corpus)
    
    def retrieve(self, query, top_k=5, w_dense=0.5, w_sparse=0.5):
        # Dense search
        query_embedding = self.encoder.encode(query)
        dense_scores = np.dot(self.embeddings, query_embedding)
        
        # Sparse search
        query_tokens = query.lower().split()
        sparse_scores = np.array(self.bm25.get_scores(query_tokens))
        
        # Normalize and combine
        dense_norm = (dense_scores - dense_scores.min()) / (dense_scores.max() - dense_scores.min() + 1e-8)
        sparse_norm = (sparse_scores - sparse_scores.min()) / (sparse_scores.max() - sparse_scores.min() + 1e-8)
        
        hybrid_scores = w_dense * dense_norm + w_sparse * sparse_norm
        
        # Rank
        top_indices = np.argsort(-hybrid_scores)[:top_k]
        
        return [(self.documents[i], hybrid_scores[i]) for i in top_indices]

# Test
documents = [
    "Order #1766 has been confirmed",
    "Order #1767 is pending",
    "Order #1765 is shipped",
    "Your account balance is $500",
]

retriever = HybridRetriever(documents)

# Test exact match
results = retriever.retrieve("Order #1766")
for doc, score in results:
    print(f"{doc}: {score:.3f}")
# Output shows Order #1766 scores highest!

# Test semantic
results = retriever.retrieve("What about my order status?")
for doc, score in results:
    print(f"{doc}: {score:.3f}")
# Also works well!
```

## Tuning Hybrid Search

### Finding the Right Balance

```python
import matplotlib.pyplot as plt

# Test different weights
weights = np.linspace(0, 1, 11)
results = []

for w_dense in weights:
    w_sparse = 1 - w_dense
    
    # Evaluate (using your own metrics)
    metric = evaluate(retriever, queries, w_dense, w_sparse)
    results.append(metric)

plt.plot(weights, results)
plt.xlabel("Weight for Dense Search")
plt.ylabel("Evaluation Metric (e.g., MRR)")
plt.title("Optimal Hybrid Balance")
plt.show()
```

## When to Use Each Approach

| Approach | When to Use |
|----------|-----------|
| Simple Sum | Quick experiments |
| Weighted Sum | Need fine-tuning, have evaluation data |
| RRF | Don't want to normalize, combining different systems |

## Summary

| Aspect | Hybrid Search |
|--------|---|
| **Solves** | Order #1766 vs #1767 problem ✅ |
| **Combines** | Dense (semantic) + Sparse (keyword) |
| **Weighting** | Tunable (0.5 / 0.5 is good start) |
| **Speed** | Still fast (parallel dense + sparse searches) |
| **Complexity** | Medium (requires two indices) |
| **Production Ready** | ✅ Yes |

## Recommendation

**Always use hybrid search for RAG unless**:
- Your queries are ONLY semantic (unlikely)
- Your queries are ONLY keyword-based (unlikely)
- Your system is extremely latency-sensitive

## Next Steps

→ [Metadata Filtering](metadata-filtering.md) — Additional safety layer for exact constraints

→ [The Exact Match Problem](../04-exact-match/hybrid-solution.md) — Full strategy with filtering

→ [Re-ranking](reranking.md) — Further improve with cross-encoders
