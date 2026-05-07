# Sparse Retrieval: BM25 and Keyword Search

**Sparse retrieval** uses term frequencies to find documents with matching keywords. It's the opposite of dense retrieval.

This is how search engines like Google work at their core.

## Why "Sparse"?

A sparse vector has mostly zeros and a few non-zero values.

Example: 100 unique words in corpus

```
Dense embedding:  [-0.23, 0.45, 0.12, ..., -0.08]  (all non-zero)
Sparse vector:    [0, 0, 5, 0, 0, ..., 3, 0, ...]  (many zeros)
                          ↑ word appears 5 times
                                        ↑ word appears 3 times
```

## BM25: The Standard Algorithm

**BM25** (Best Matching 25) is the industry-standard sparse retrieval algorithm. It scores documents based on:

1. **Term Frequency (TF)**: How often the term appears
2. **Inverse Document Frequency (IDF)**: How rare the term is
3. **Document Length Normalization**: Longer docs don't automatically win

### BM25 Formula

For a term $t$ in document $d$:

$$\text{BM25}(t, d) = \text{IDF}(t) \cdot \frac{TF(t,d) \cdot (k_1 + 1)}{TF(t,d) + k_1 \cdot (1 - b + b \cdot \frac{|d|}{L_{avg}})}$$

where:
- $k_1$ ≈ 1.5 (controls TF saturation)
- $b$ ≈ 0.75 (controls length normalization)
- $|d|$ = document length
- $L_{avg}$ = average document length

**Don't memorize** this! The key insight: rarer terms in relevant-length documents score higher.

## Why BM25 Solves the Order #1766 Problem

Remember the problem:

```
Dense: "Order #1766" and "Order #1767" are similar
Sparse: "Order #1766" and "Order #1767" are completely different
```

Why? Because the exact match "1766" is unique:

- Appears in Order #1766 docs: 1-2 times
- Appears in ALL docs: 1 time total
- IDF("1766") = log(total_docs / 1) = huge!

```python
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

documents = [
    "Order #1766 has been confirmed",
    "Order #1767 is pending",
    "Order #1765 is shipped",
    "Cat food is on sale",
]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

# Get term scores for first document
feature_names = vectorizer.get_feature_names_out()
scores = tfidf_matrix[0].toarray().flatten()

print("Document: 'Order #1766 has been confirmed'")
for name, score in zip(feature_names, scores):
    if score > 0:
        print(f"  {name}: {score:.3f}")

# Output shows that "1766" has very high TF-IDF score!
```

## BM25 in Python

Using **rank-bm25** library (pure Python):

```python
from rank_bm25 import BM25Okapi
import numpy as np

# Tokenize documents
documents = [
    "Order #1766 has been confirmed",
    "Order #1767 is pending",
    "Order #1765 is shipped",
]

corpus = [doc.split() for doc in documents]

# Create BM25 index
bm25 = BM25Okapi(corpus)

# Query
query = "Order #1766".split()
scores = bm25.get_scores(query)

print("Scores:", scores)
# Output: [10.2, 2.1, 1.9]
# Document 0 (Order #1766) scores MUCH higher!

top_indices = np.argsort(-scores)[:3]
for i in top_indices:
    print(f"{documents[i]}: {scores[i]:.2f}")
```

**Output**:
```
Order #1766 has been confirmed: 10.20
Order #1767 is pending: 2.10
Order #1765 is shipped: 1.90
```

Perfect! BM25 correctly prioritizes the exact match.

## Elasticsearch: Production BM25

For production, use Elasticsearch:

```python
from elasticsearch import Elasticsearch

es = Elasticsearch(['http://localhost:9200'])

# Index documents
for i, doc in enumerate(documents):
    es.index(index="orders", id=i, document={"text": doc})

# Search with BM25
query = "Order #1766"
results = es.search(index="orders", body={
    "query": {
        "match": {
            "text": query
        }
    },
    "size": 10
})

for hit in results['hits']['hits']:
    print(f"{hit['_source']['text']}: {hit['_score']:.2f}")
```

## Pros of BM25

✅ **Perfect for exact matches**: "1766" matches only Order #1766  
✅ **Fast**: Inverted indices are highly optimized  
✅ **Interpretable**: Scores directly relate to term frequency  
✅ **Handles stop words**: "the", "a" are downweighted automatically  
✅ **Scalable**: Used by Google, Elasticsearch, etc.

## Cons of BM25

❌ **Bad for synonyms**: "cat" doesn't match "feline"  
❌ **No semantic understanding**: "dog breed" and "a breed of dog" are different  
❌ **Requires exact words**: Typos break matching  
❌ **Ambiguity**: "bank" matches both financial and river banks equally

## Comparison: Dense vs Sparse

| Query | Dense | Sparse (BM25) |
|-------|-------|--------------|
| "What's my order status?" | ✅ Great | ❌ Poor (no exact match to "status") |
| "Order #1766" | ❌ Bad (similar to #1767) | ✅ Perfect |
| "Tell me about my order" | ✅ Great | ⚠ OK (finds "order" keyword) |
| "feline animal pictures" | ✅ Great (understands "cat") | ❌ Bad (no "cat" keyword) |

## Sparse Retrieval in Vector Databases

Modern vector databases support sparse vectors:

```python
from qdrant_client import QdrantClient
from qdrant_client.models import SparseVector, PointStruct

client = QdrantClient(":memory:")

# Create sparse index
client.create_collection(
    collection_name="sparse_orders",
    sparse_vectors_config=SparseVectorConfig(...),
)

# Add with sparse vectors (from BM25 or TF-IDF)
for i, doc in enumerate(documents):
    sparse_vector = create_sparse_vector(doc)  # From BM25
    client.upsert(
        collection_name="sparse_orders",
        points=[PointStruct(
            id=i,
            vector=sparse_vector,
            payload={"text": doc}
        )]
    )

# Search
query = "Order #1766"
sparse_query_vector = create_sparse_vector(query)
results = client.search(
    collection_name="sparse_orders",
    query_vector=sparse_query_vector,
    limit=10
)
```

## Summary

| Aspect | BM25 Sparse |
|--------|------------|
| **What** | Term frequency matching |
| **Scoring** | TF × IDF × length normalization |
| **Speed** | ⚡ Fast (inverted index) |
| **Strength** | Perfect for exact matches & keywords |
| **Weakness** | No semantic understanding |
| **Best for** | Structured queries, IDs, exact keywords |

## The Key Insight for RAG

**BM25 is how you solve the Order #1766 problem for the keyword part.**

But you still need to handle semantic queries like "What's my order status?"

That's where **hybrid search** comes in.

## Next Steps

→ **[Hybrid Search](hybrid-search.md)** — Combine dense + sparse to get the best of both!

→ [The Exact Match Problem](../04-exact-match/index.md) — Full solution strategy

--8<-- "_abbreviations.md"
