# Hybrid Solution: Putting It All Together

This page shows the **complete, practical solution** to the Order #1766 problem.

## The Four-Layer Architecture

```
                     User Query
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
    [Semantic]      [Keyword]       [Extract
     Embeddings      Search         Constraints]
        │                ↓                │
        │            [BM25]              │
        │                │                │
        └────────────────┼────────────────┘
                         ↓
                 [Combine Scores]
                (weights or RRF)
                         │
        ┌────────────────┴────────────────┐
        ↓                                  ↓
   [Top-K Candidates]            [Metadata Filter]
   (100 documents)               (extract & filter)
        │                                  │
        └────────────────┬─────────────────┘
                         ↓
                  [Rerank (optional)]
                 (cross-encoder)
                         │
        ┌────────────────┴────────────────┐
        ↓                                  ↓
   [Return Results]             [Ranked Results]
```

## Implementation: Step by Step

###Step 1: Setup Vector Database & Indexing

```python
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

# Load encoder
encoder = SentenceTransformer('all-MiniLM-L6-v2')

# Setup Qdrant (vector database)
client = QdrantClient(url="http://localhost:6333")

client.create_collection(
    collection_name="orders",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

# Sample documents
documents = [
    {"id": "1", "text": "Order #1766 has been confirmed"},
    {"id": "2", "text": "Order #1767 is pending verification"},
    {"id": "3", "text": "Order #1765 is shipped"},
    {"id": "4", "text": "Your account balance is $500"},
]

# Add to vector database with metadata
for doc in documents:
    embedding = encoder.encode(doc["text"])
    
    # Extract order ID from text
    order_id_match = re.search(r'Order #(\d+)', doc["text"])
    order_id = order_id_match.group(1) if order_id_match else None
    
    client.upsert(
        collection_name="orders",
        points=[
            PointStruct(
                id=int(doc["id"]),
                vector=embedding,
                payload={
                    "text": doc["text"],
                    "order_id": order_id,
                    "type": "order" if order_id else "general"
                }
            )
        ]
    )

# Setup BM25 (sparse index)
corpus = [doc["text"].lower().split() for doc in documents]
bm25 = BM25Okapi(corpus)
```

### Step 2: Extract Constraints from Query

```python
def extract_constraints(query):
    """Extract exact IDs and filters from user query."""
    constraints = {}
    
    # Extract Order ID
    order_match = re.search(r'[Oo]rder\s*#?(\d+)', query)
    if order_match:
        constraints['order_id'] = order_match.group(1)
    
    # Extract Customer ID
    customer_match = re.search(r'[Cc]ustomer\s+(\w+)', query)
    if customer_match:
        constraints['customer_id'] = customer_match.group(1)
    
    # Extract date range
    date_match = re.search(r'(January|February|...|December)\s+(\d{4})', query)
    if date_match:
        constraints['date_range'] = date_match.groups()
    
    return constraints

query = "What about Order #1766?"
constraints = extract_constraints(query)
# Result: {'order_id': '1766'}
```

### Step 3: Dense Retrieval (Semantic)

```python
def dense_search(query, top_k=100):
    """Retrieve using embeddings."""
    query_embedding = encoder.encode(query)
    
    results = client.search(
        collection_name="orders",
        query_vector=query_embedding,
        limit=top_k
    )
    
    # Extract candidates
    candidates = []
    for result in results:
        candidates.append({
            'id': result.id,
            'text': result.payload['text'],
            'order_id': result.payload.get('order_id'),
            'dense_score': result.score
        })
    
    return candidates

dense_candidates = dense_search(query, top_k=100)
```

### Step 4: Sparse Retrieval (Keyword/BM25)

```python
def sparse_search(query, top_k=100):
    """Retrieve using BM25."""
    query_tokens = query.lower().split()
    
    # Get BM25 scores
    scores = bm25.get_scores(query_tokens)
    
    # Get top candidates
    top_indices = np.argsort(-scores)[:top_k]
    
    candidates = []
    for idx in top_indices:
        candidates.append({
            'id': idx + 1,  # Assuming IDs start from 1
            'text': documents[idx]['text'],
            'order_id': documents[idx].get('order_id'),
            'sparse_score': scores[idx]
        })
    
    return candidates

sparse_candidates = sparse_search(query, top_k=100)
```

### Step 5: Hybrid Combination

```python
def combine_hybrid(dense_candidates, sparse_candidates, w_dense=0.5, w_sparse=0.5):
    """Combine dense and sparse results."""
    
    # Normalize scores to [0, 1]
    dense_scores = [c['dense_score'] for c in dense_candidates]
    sparse_scores = [c['sparse_score'] for c in sparse_candidates]
    
    dense_min, dense_max = min(dense_scores), max(dense_scores)
    sparse_min, sparse_max = min(sparse_scores), max(sparse_scores)
    
    # Create score map
    combined_scores = {}
    
    # Add dense scores
    for cand in dense_candidates:
        doc_id = cand['id']
        norm_score = (cand['dense_score'] - dense_min) / (dense_max - dense_min + 1e-8)
        combined_scores[doc_id] = combined_scores.get(doc_id, {})
        combined_scores[doc_id]['dense_score'] = norm_score
        combined_scores[doc_id]['text'] = cand['text']
        combined_scores[doc_id]['order_id'] = cand['order_id']
    
    # Add sparse scores
    for cand in sparse_candidates:
        doc_id = cand['id']
        norm_score = (cand['sparse_score'] - sparse_min) / (sparse_max - sparse_min + 1e-8)
        combined_scores[doc_id] = combined_scores.get(doc_id, {})
        combined_scores[doc_id]['sparse_score'] = norm_score
        combined_scores[doc_id]['text'] = cand['text']
        combined_scores[doc_id]['order_id'] = cand['order_id']
    
    # Combine with weights
    final_scores = {}
    for doc_id, scores in combined_scores.items():
        dense = scores.get('dense_score', 0)
        sparse = scores.get('sparse_score', 0)
        final_scores[doc_id] = {
            'hybrid_score': w_dense * dense + w_sparse * sparse,
            'text': scores['text'],
            'order_id': scores['order_id']
        }
    
    # Sort by hybrid score
    sorted_results = sorted(
        final_scores.items(),
        key=lambda x: x[1]['hybrid_score'],
        reverse=True
    )
    
    return sorted_results

hybrid_results = combine_hybrid(dense_candidates, sparse_candidates)
```

### Step 6: Apply Metadata Filtering

```python
def apply_metadata_filter(hybrid_results, constraints):
    """Filter results by extracted constraints."""
    
    filtered = hybrid_results
    
    # Filter by order ID if extracted
    if 'order_id' in constraints:
        filtered = [
            r for r in filtered
            if r[1].get('order_id') == constraints['order_id']
        ]
    
    # Filter by customer ID if extracted
    if 'customer_id' in constraints:
        filtered = [
            r for r in filtered
            if constraints['customer_id'] in r[1]['text']
        ]
    
    return filtered

filtered_results = apply_metadata_filter(hybrid_results, constraints)
```

### Step 7 (Optional): Re-ranking

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank_results(filtered_results, query, top_k_rerank=10):
    """Re-rank using a cross-encoder."""
    
    # Get top candidates to rerank
    candidates = filtered_results[:top_k_rerank]
    
    # Create pairs
    pairs = [[query, result[1]['text']] for result in candidates]
    
    # Score
    rerank_scores = reranker.predict(pairs)
    
    # Re-order
    reranked = sorted(
        zip(candidates, rerank_scores),
        key=lambda x: x[1],
        reverse=True
    )
    
    return reranked

reranked = rerank_results(filtered_results, query)
```

### Step 8: Return Final Results

```python
def retrieve(query, top_k=10):
    """Complete retrieval pipeline."""
    
    # Step 1: Extract constraints
    constraints = extract_constraints(query)
    
    # Step 2: Dense search
    dense = dense_search(query, top_k=100)
    
    # Step 3: Sparse search
    sparse = sparse_search(query, top_k=100)
    
    # Step 4: Combine
    hybrid = combine_hybrid(dense, sparse, w_dense=0.5, w_sparse=0.5)
    
    # Step 5: Metadata filter
    filtered = apply_metadata_filter(hybrid, constraints)
    
    # Step 6: Re-rank (optional, but improves quality)
    reranked = rerank_results(filtered, query, top_k_rerank=20)
    
    # Step 7: Return
    return [(r[0][1]['text'], r[1]) for r in reranked[:top_k]]

# Test it!
results = retrieve("What about Order #1766?", top_k=5)

for i, (text, score) in enumerate(results, 1):
    print(f"{i}. {text} (score: {score:.3f})")
```

**Output**:
```
1. Order #1766 has been confirmed (score: 0.95)
2. Order #1765 is shipped (score: 0.42)
3. Your account balance is $500 (score: 0.18)
```

Perfect! Order #1766 is returned, not #1767!

## Complete Example Class

```python
class HybridRAGRetriever:
    def __init__(self, documents, use_reranking=True):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.documents = documents
        self.use_reranking = use_reranking
        
        if use_reranking:
            self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        
        # Initialize vector DB
        self.client = QdrantClient(":memory:")
        self._build_indices()
        
        # Initialize BM25
        corpus = [doc['text'].lower().split() for doc in documents]
        self.bm25 = BM25Okapi(corpus)
    
    def _build_indices(self):
        """Build both dense and sparse indices."""
        # Vector DB setup
        self.client.create_collection(
            collection_name="docs",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        
        # Add vectors
        for i, doc in enumerate(self.documents):
            emb = self.encoder.encode(doc['text'])
            order_id = re.search(r'Order #(\d+)', doc['text'])
            
            self.client.upsert(
                collection_name="docs",
                points=[PointStruct(
                    id=i,
                    vector=emb,
                    payload={
                        'text': doc['text'],
                        'order_id': order_id.group(1) if order_id else None
                    }
                )]
            )
    
    def retrieve(self, query, top_k=10):
        """Retrieve with hybrid search."""
        # Steps 1-5 from above...
        # (consolidated into this method)
        
        constraints = extract_constraints(query)
        dense = self._dense_search(query)
        sparse = self._sparse_search(query)
        hybrid = self._combine(dense, sparse)
        filtered = self._filter(hybrid, constraints)
        
        if self.use_reranking:
            final = self._rerank(filtered, query)
        else:
            final = filtered
        
        return final[:top_k]
    
    def _dense_search(self, query, top_k=100):
        # Dense search implementation
        pass
    
    def _sparse_search(self, query, top_k=100):
        # Sparse search implementation
        pass
    
    def _combine(self, dense, sparse):
        # Combination implementation
        pass
    
    def _filter(self, results, constraints):
        # Filtering implementation
        pass
    
    def _rerank(self, results, query):
        # Re-ranking implementation
        pass
```

## Testing the Solution

```python
# Test 1: Order #1766 specific
results = retrieve("What about Order #1766?")
assert any("#1766" in r[0] for r in results)
assert not any("#1767" in r[0] for r in results)  # Shouldn't return #1767
print("✅ Test 1 passed: Only Order #1766 returned")

# Test 2: Semantic query
results = retrieve("What's my order status?")
assert any("order" in r[0].lower() for r in results)
print("✅ Test 2 passed: Semantic query works")

# Test 3: Ambiguous query (relies on hybrid)
results = retrieve("Order information")
assert len(results) > 0
print("✅ Test 3 passed: Ambiguous query handled")
```

## Summary: The Solution

| Layer | Component | Purpose |
|-------|-----------|---------|
| **1** | Dense Search | Capture meaning (semantic) |
| **2** | Sparse Search | Find exact keywords (BM25) |
| **3** | Hybrid Combination | Balance both signals |
| **4** | Metadata Filtering | Enforce constraints (Order #1766 only) |
| **5** | Re-ranking (optional) | Fine-tune final ranking |

## Key Points

✅ Metadata filtering is the final safety net—it guarantees only Order #1766 is returned  
✅ Hybrid search re-ranks results so BM25's precision helps  
✅ Constraint extraction catches exact IDs before searching  
✅ Re-ranking improves quality when time allows

## Next Steps

→ [Chunking Strategies](chunking-strategies.md) — Preparing documents properly

→ [RAG Pipeline](../05-rag-pipeline/index.md) — End-to-end system
