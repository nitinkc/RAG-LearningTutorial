# Metadata Filtering: Enforcing Hard Constraints

Metadata filtering adds another layer: **filter by structured properties before or after similarity search**.

This is especially important for the Order #1766 problem.

## The Concept

Store structured information alongside embeddings:

```
Document: "Your Order #1766 shipped via FedEx"
    ├─ Text (embedded): "Your Order #1766 shipped via FedEx"
    └─ Metadata (structured):
        ├─ order_id: "1766"
        ├─ status: "shipped"
        ├─ carrier: "fedex"
        └─ created_date: "2024-01-15"
```

## Strategies

### Strategy 1: Pre-Filtering (Filter → Search)

Filter documents by metadata **before** similarity search:

```python
# Only consider Order #1766 documents
filtered_docs = [doc for doc in all_docs if doc.metadata['order_id'] == '1766']

# Then search within this subset
results = semantic_search(query, filtered_docs)
```

**Pros**: Reduces search space, guarantees only relevant docs  
**Cons**: Need to know filter criteria upfront

### Strategy 2: Post-Filtering (Search → Filter)

Perform similarity search first, then filter results:

```python
# Search across all documents
all_results = semantic_search(query, all_docs, top_k=100)

# Then filter results
filtered_results = [r for r in all_results if r.metadata['order_id'] == '1766']

# Return top-k from filtered
return filtered_results[:10]
```

**Pros**: Flexible, can apply multiple filters  
**Cons**: Might not return enough results if many are filtered out

### Strategy 3: Integrated Filtering (Search with Constraints)

Modern vector databases let you specify filters within queries:

```python
# Qdrant example
results = client.search(
    collection_name="orders",
    query_vector=query_embedding,
    limit=10,
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="order_id",
                match=models.MatchValue(value="1766")
            )
        ]
    )
)
```

**Pros**: Most efficient, enforced at index level  
**Cons**: Requires vector database support

## Metadata Filter Types

### Exact Match

```python
# Find documents with exact order ID
filter = {"order_id": {"$eq": "1766"}}

# Elasticsearch
{"term": {"order_id": "1766"}}

# Qdrant
models.MatchValue(value="1766")
```

### Range

```python
# Find orders placed in 2024
filter = {"created_date": {"$gte": "2024-01-01", "$lt": "2025-01-01"}}

# Elasticsearch
{"range": {"created_date": {"gte": "2024-01-01"}}}

# Qdrant
models.RangeCondition(gte=1704067200, lt=1735689600)
```

### In List

```python
# Find orders with status in ['shipped', 'delivered']
filter = {"status": {"$in": ["shipped", "delivered"]}}

# Elasticsearch
{"terms": {"status": ["shipped", "delivered"]}}

# Qdrant
models.HasIdCondition(has_id=[1, 2, 3])
```

### Boolean Combinations

```python
# (order_id = "1766") AND (status = "shipped")
filter = {
    "$and": [
        {"order_id": {"$eq": "1766"}},
        {"status": {"$eq": "shipped"}}
    ]
}

# (order_id = "1766") OR (order_id = "1767")
filter = {
    "$or": [
        {"order_id": {"$eq": "1766"}},
        {"order_id": {"$eq": "1767"}}
    ]
}
```

## The Key Solution for Order #1766

```python
# User asks: "What about order 1766?"

# Step 1: Extract order ID from query
order_id = extract_order_id(query)  # Returns "1766"

# Step 2: Create metadata filter
metadata_filter = {
    "order_id": {"$eq": order_id}
}

# Step 3: Search with filter
results = vector_db.search(
    query_embedding,
    filter=metadata_filter,
    top_k=10
)

# Result: ONLY Order #1766 documents returned, not #1767!
```

## Example: Chroma with Metadata Filtering

```python
import chromadb

client = chromadb.Client()
collection = client.create_collection(name="orders")

# Add documents with metadata
collection.add(
    ids=["1", "2", "3"],
    documents=[
        "Order #1766 has been confirmed",
        "Order #1767 is pending",
        "Order #1766 tracking info available"
    ],
    metadatas=[
        {"order_id": "1766", "status": "confirmed"},
        {"order_id": "1767", "status": "pending"},
        {"order_id": "1766", "status": "confirmed"}
    ]
)

# Query with metadata filter
results = collection.query(
    query_texts=["What about my order?"],
    n_results=5,
    where={"order_id": {"$eq": "1766"}}  # Filter!
)

# Returns ONLY Order #1766 documents
```

## Example: Qdrant with Metadata Filtering

```python
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, MatchValue, Filter, PointStruct

client = QdrantClient(":memory:")

# Create collection and add points with metadata
client.create_collection(
    collection_name="orders",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

client.upsert(
    collection_name="orders",
    points=[
        PointStruct(
            id=1,
            vector=[0.1]*384,
            payload={"order_id": "1766", "status": "confirmed"}
        ),
        PointStruct(
            id=2,
            vector=[0.11]*384,
            payload={"order_id": "1767", "status": "pending"}
        ),
    ]
)

# Search with metadata filter
results = client.search(
    collection_name="orders",
    query_vector=[0.12]*384,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="order_id",
                match=MatchValue(value="1766")
            )
        ]
    ),
    limit=10
)
```

## Combining Filtering Strategies

**Best practice**: Use all three layers:

```python
class SmartRetriever:
    def retrieve(self, query, user_context):
        # Layer 1: Extract constraints from query
        order_id = extract_order_id(query)
        
        # Layer 2: Metadata filter (hard constraint)
        metadata_filter = None
        if order_id:
           metadata_filter = {"order_id": {"$eq": order_id}}
        
        # Layer 3: Hybrid search (dense + sparse)
        dense_results = self.dense_search(query, filter=metadata_filter)
        sparse_results = self.bm25_search(query, filter=metadata_filter)
        
        # Layer 4: Combine
        hybrid_results = self.combine(dense_results, sparse_results)
        
        return hybrid_results
```

## Performance Considerations

### Pre-filtering

```
1,000,000 documents
├─ Filter: order_id = "1766" 
│  ├─ Remaining: ~10 docs
│  └─ Search in 10: very fast
```

Good when filters significantly reduce search space.

### Post-filtering

```
1,000,000 documents
├─ Search in all: ~100ms
├─ Filter results: instant
└─ Might lose results if top-k all filtered out
```

Good when filters are loose.

### Integrated filtering

```
1,000,000 documents
├─ Index structure optimized for filters
└─ Search within filtered index: fastest
```

Best when available.

## Metadata Best Practices

### What to Store

```python
metadata = {
    # For filtering (store efficiently)
    "order_id": "1766",              # String
    "status": "shipped",              # Enum
    "customer_id": "123",             # String
    "created_timestamp": 1704067200,  # Unix timestamp (searchable range)
    
    # For context/display (don't need to filter)
    "customer_name": "John Doe",      # Can be in text
    "total_amount": "$99.99",         # Can be in text
}
```

### Indexing Strategy

```python
# Index fields you'll filter on
# Don't index fields you won't filter on

# Good: Small, exact values
"order_id": "1766"
"status": "shipped"

# Bad: Large text values
"full_order_description": "Order #1766 ..."  # Use in documents instead
```

## Summary

| Strategy | When to Use | Pros | Cons |
|----------|-----------|------|------|
| **Pre-filter** | Extractable filters from query | Fastest | Requires upfront extraction |
| **Post-filter** | Flexible filters | Simple | Might miss results |
| **Integrated** | Vector DB supports it | Most efficient | Requires specific DB |

## Key Insight for Order #1766

**Exact ID matching should ALWAYS use metadata filters, never semantic similarity.**

```python
# ❌ WRONG (semantic matching might fail)
results = semantic_search(query)  # Might return #1767

# ✅ RIGHT (use metadata filter)
if "1766" in query:
    results = semantic_search(
        query,
        filter={"order_id": "1766"}
    )
```

## Next Steps

→ [Re-ranking](reranking.md) — Improve result quality further

→ [The Exact Match Problem](../04-exact-match/hybrid-solution.md) — Putting it all together
