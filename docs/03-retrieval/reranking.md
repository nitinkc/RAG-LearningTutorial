# Re-ranking: Improving Result Quality

After retrieving candidates with dense + sparse + filtering, **re-ranking** uses a more powerful model to reorder results.

## The Concept

```
Initial Retrieval (fast, finds ~100 candidates):
├─ Document A: score 0.87
├─ Document B: score 0.85
├─ Document C: score 0.84
└─ ... 97 more

Cross-Encoder Re-ranking (slower, ranks top 10):
├─ Document A: score 0.95  (was #1)
├─ Document C: score 0.92  (was #3)
└─ Document B: score 0.88  (was #2)

User gets Document C as #2 instead of #3 - better results!
```

## Why Re-ranking Works

**Retrieval models** (embeddings) are optimized for:

- ✅ Speed (must process thousands of candidates)
- ❌ Precision (might miss subtle relevance)

**Re-ranking models** (cross-encoders) are optimized for:

- ❌ Speed (only process top-K candidates)
- ✅ Precision (deeply understand query-document pairs)

## Dense (Bi-encoder) vs Cross-Encoder

### Bi-encoders (Retrieval)

Vectors created independently:

```
Query: "Order #1766 status"
    ↓
[Encoder]
    ↓
Query embedding: [0.1, 0.2, 0.3, ...]

Document: "Order #1766 shipped"
    ↓
[Encoder]
    ↓
Document embedding: [0.11, 0.19, 0.32, ...]

Score: cosine_similarity(query, document) = 0.98
```

**Pros**: Fast (precompute document embeddings once)

**Cons**: Can't use query context to understand document

### Cross-encoders (Re-ranking)

Vectors created together:

```
Query + Document (concatenated): "Order #1766 status [SEP] Order #1766 shipped"
    ↓
[Model - processes both together]
    ↓
Relevance score: 0.95
```

**Pros**: Can understand subtle interactions between query and document  
**Cons**: Slow (must run for each query-document pair)

## Cross-Encoder Models

Popular pre-trained cross-encoders:

### Sentence Transformers Cross-Encoders

```python
from sentence_transformers import CrossEncoder

# Load model
model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# Score query-document pairs
pairs = [
    ["Order #1766 status", "Order #1766 has been shipped"],
    ["Order #1766 status", "Order #1767 is pending"],
    ["Order #1766 status", "Your account balance is $500"],
]

scores = model.predict(pairs)
print(scores)  # [0.95, 0.23, 0.12]
```

### Models for Different Tasks

| Model | Domain | Size |
|-------|--------|------|
| `cross-encoder/ms-marco-MiniLM-L-6-v2` | General | Fast |
| `cross-encoder/qnli-distilroberta-base` | Question-answering | Medium |
| `cross-encoder/ms-marco-TinyBERT-L-2-v2` | Very fast | ultrafast |
| `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` | Multilingual | Medium |

## Implementation: Basic Re-ranking

```python
from sentence_transformers import SentenceTransformer, CrossEncoder
import numpy as np

# Step 1: Dense retrieval (fast, ~100 candidates)
retriever = SentenceTransformer('all-MiniLM-L6-v2')

query = "Order #1766 status"
documents = [
    "Order #1766 has been shipped",
    "Order #1767 is pending",
    "Order #1765 will arrive tomorrow",
    "Your account balance is $500",
]

# Initial retrieval
query_embedding = retriever.encode(query)
doc_embeddings = retriever.encode(documents)

# Cosine similarity (approximate)
from sklearn.metrics.pairwise import cosine_similarity
initial_scores = cosine_similarity([query_embedding], doc_embeddings)[0]

# Get top-20 candidates
top_k_initial = 20
top_indices = np.argsort(-initial_scores)[:min(top_k_initial, len(documents))]

# Step 2: Cross-encoder re-ranking (slow, ~10 final results)
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# Create pairs for re-ranking
candidate_docs = [documents[i] for i in top_indices]
pairs = [[query, doc] for doc in candidate_docs]

# Get refined scores
rerank_scores = reranker.predict(pairs)

# Re-rank
reranked_indices = np.argsort(-rerank_scores)

# Return top-10
final_results = [(candidate_docs[i], rerank_scores[i]) for i in reranked_indices[:10]]

for doc, score in final_results:
    print(f"{doc}: {score:.3f}")
```

**Output**:
```
Order #1766 has been shipped: 0.95
Order #1765 will arrive tomorrow: 0.42
Order #1767 is pending: 0.35
Your account balance is $500: 0.12
```

## Hybrid + Re-ranking Pipeline (Complete)

```python
class AdvancedRAGRetriever:
    def __init__(self):
        # Dense retriever
        self.dense = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Sparse retriever (BM25)
        self.bm25 = BM25Okapi(corpus)
        
        # Re-ranker
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    
    def retrieve(self, query, top_k_final=10):
        # Step 1: Dense retrieval (get 100 candidates)
        query_embedding = self.dense.encode(query)
        dense_scores = cosine_scores(query_embedding, all_embeddings)
        dense_candidates = get_top_k(dense_scores, k=100)
        
        # Step 2: Sparse retrieval (get 100 candidates)
        query_tokens = tokenize(query)
        sparse_scores = self.bm25.get_scores(query_tokens)
        sparse_candidates = get_top_k(sparse_scores, k=100)
        
        # Step 3: Hybrid combination (combine to get ~100 unique candidates)
        candidates = combine_results(dense_candidates, sparse_candidates)
        
        # Step 4: Metadata filtering
        filtered_candidates = apply_metadata_filter(candidates, query)
        
        # Step 5: Re-ranking (re-score top candidates)
        pairs = [[query, doc] for doc in filtered_candidates]
        rerank_scores = self.reranker.predict(pairs)
        
        # Step 6: Return final results
        final_indices = np.argsort(-rerank_scores)[:top_k_final]
        return [filtered_candidates[i] for i in final_indices]
```

## When to Use Re-ranking

| Scenario | Use Re-ranking? | Cost |
|----------|---|---|
| Real-time search (< 100ms latency) | ❌ No (too slow) | - |
| Batch search, high quality needed | ✅ Yes | +50ms per query |
| FAQ/document search | ✅ Yes | + minimal |
| Exact matching (Order #1766) | ⚠ Maybe (metadata filter sufficient) | - |

## Trade-offs: Latency vs Quality

```
Retrieval only (bi-encoder): 50ms, quality ~80%
+ Re-ranking (cross-encoder): +50ms = 100ms total, quality ~92%
+ LLM rewriting: +200ms = 300ms total, quality ~95%
```

For real-time applications:  
- Use retrieval + filtering (50ms is OK)

For batch/offline:
- Add re-ranking (quality improves significantly)

## Practical Considerations

### Batching for Efficiency

```python
# Don't score  one pair at a time
# Instead, batch multiple pairs

query = "Order #1766"

# Batch all candidates at once
all_pairs = [[query, doc] for doc in candidates]
scores = reranker.predict(all_pairs)  # Much faster than loop!
```

### Using Text Truncation

Cross-encoders have input limits (usually 512 tokens):

```python
# Truncate long documents
def truncate(text, max_length=512):
    tokens = tokenizer.encode(text)
    return tokenizer.decode(tokens[:max_length])

pairs = [[query, truncate(doc)] for doc in candidates]
```

### GPU Acceleration

Cross-encoders are neural networks—use GPU for speed:

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', device='cuda')

# Now predictions use GPU (10x faster)
scores = model.predict(pairs)
```

## Summary

| Approach | Speed | Quality | Best For |
|----------|-------|---------|----------|
| **Dense only** | 🚀 Fast | ⚠ ~80% | Real-time |
| **Dense + Sparse** | ⚡ Medium | ⚠ ~85% | Most cases |
| **+ Re-ranking** | 🐢 Slow | ✅ ~92% | Batch/offline |
| **+ Metadata filter** | ✅ Depends | ✅ Perfect | Exact matches |

## Design Recommendation

```
┌─ Dense + Sparse (Hybrid)
│  │
│  ├─ Metadata Filtering
│  │
│  └─ Re-ranking (if time allows / if batch)
│
└─ Return final results
```

## Next Steps

→ [The Exact Match Problem](../04-exact-match/index.md) — Putting all pieces together

→ [RAG Pipeline](../05-rag-pipeline/index.md) — End-to-end system

--8<-- "_abbreviations.md"
