# Vector Databases and Production Systems

Vector databases are specialized systems designed for efficiently storing and searching **embeddings** at scale.

## What Is a Vector Database?

A system that:

1. **Stores** millions/billions of vectors and their metadata
2. **Indexes** them for fast similarity search (using HNSW, IVF, etc.)
3. **Provides filtering** (find similar vectors WHERE metadata matches)
4. **Handles updates** (add/delete vectors)
5. **Scales** across machines

## Popular Vector Databases

### FAISS (Facebook AI Similarity Search)

**Type**: Library (not a full database)  
**Cost**: Free, open-source  
**Best for**: Learning, prototyping, single-machine deployments

```python
import faiss
import numpy as np

# Create vectors
vectors = np.random.randn(100000, 384).astype('float32')

# Create index
index = faiss.IndexHNSWFlat(384, 32)
index.add(vectors)

# Search
query = np.random.randn(1, 384).astype('float32')
distances, indices = index.search(query, k=10)
```

**Pros**: Simple, fast, embeddable  
**Cons**: No network access, no metadata filtering, single-machine

### Chroma

**Type**: Full database  
**Cost**: Free, open-source  
**Best for**: Small-to-medium RAG projects, embedding databases

```python
import chromadb

client = chromadb.Client()
collection = client.create_collection(name="my_collection")

# Add documents with metadata
collection.add(
    ids=["1", "2", "3"],
    documents=[
        "This is a document about cats",
        "This is about dogs",
        "This is about birds"
    ],
    metadatas=[
        {"source": "wiki"},
        {"source": "blog"},
        {"source": "journal"}
    ]
)

# Query
results = collection.query(
    query_texts=["I like animals"],
    n_results=3
)
```

**Pros**: Easy to use, SQLite backend, metadata filtering  
**Cons**: Limited to single machine, slower for millions of vectors

### Weaviate

**Type**: Full database  
**Cost**: Open-source + cloud pricing  
**Best for**: Production RAG, multi-tenant systems

```python
import weaviate

client = weaviate.Client("http://localhost:8080")

# Create class
client.schema.create_class({
    "class": "Document",
    "properties": [
        {"name": "content", "dataType": ["text"]},
        {"name": "order_id", "dataType": ["string"]}
    ]
})

# Add objects
client.batch.add_data_object(
    {"content": "Order #1766 placed", "order_id": "1766"},
    "Document"
)

# Search with filter
results = client.query.get("Document", ["content"]).with_near_text({
    "concepts": ["order status"]
}).with_where({
    "path": ["order_id"],
    "operator": "Equal",
    "valueString": "1766"
}).do()
```

**Pros**: Distributed, metadata filtering, GraphQL API, multi-tenant  
**Cons**: More complex, requires deployment

### Pinecone

**Type**: Managed cloud database  
**Cost**: Serverless pricing ($0.04/million vectors/month + queries)  
**Best for**: Production RAG without managing infrastructure

```python
from pinecone import Pinecone

pc = Pinecone(api_key="your-api-key")
index = pc.Index("my-index")

# Upsert vectors with metadata
index.upsert(vectors=[
    ("vec-1", [0.1, 0.2, 0.3], {"order_id": "1766"}),
    ("vec-2", [0.4, 0.5, 0.6], {"order_id": "1767"}),
])

# Query with metadata filter
results = index.query(
    vector=[0.15, 0.25, 0.35],
    top_k=10,
    filter={"order_id": {"$eq": "1766"}}
)
```

**Pros**: Fully managed, scales automatically, good integrations  
**Cons**: Vendor lock-in, cost at scale, data privacy concerns

### Qdrant

**Type**: Full database  
**Cost**: Open-source + cloud  
**Best for**: Production RAG, on-premises deployments

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient(":memory:")

# Create collection
client.create_collection(
    collection_name="orders",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

# Upsert points
client.upsert(
    collection_name="orders",
    points=[
        PointStruct(id=1, vector=[0.1]*384, payload={"order_id": "1766"}),
        PointStruct(id=2, vector=[0.2]*384, payload={"order_id": "1767"}),
    ]
)

# Search with filter
client.search(
    collection_name="orders",
    query_vector......[0.15]*384,
    query_filter=models.Filter(
        must=[
            models.HasIdCondition(has_id=[1])
        ]
    ),
    limit=10
)
```

**Pros**: Distributed, good filtering, performance, open-source  
**Cons**: Requires deployment, newer ecosystem

## Comparison Table

| Database | Type | Cost | Scale | Filtering | Best For |
|----------|------|------|-------|-----------|----------|
| **FAISS** | Library | Free | Single machine | None | Learning |
| **Chroma** | Database | Free | < 1M vectors | Basic | Small RAG |
| **Weaviate** | Database | Free/$ | Billions | GraphQL | Production |
| **Pinecone** | Managed | $$/pay-as-go | Billions | Advanced | Cloud-native |
| **Qdrant** | Database | Free/$ | Billions | SQL-like | On-prem |
| **Milvus** | Database | Free | Billions | SQL | Large scale |

## Which One to Choose?

**Decision Tree**:

```
Are you in production?
├─ NO (prototyping)
│  └─ Use FAISS or Chroma (simple, free)
│
└─ YES
   ├─ Prefer managed cloud?
   │  └─ Use Pinecone (simplest)
   │
   ├─ Have infrastructure team?
   │  └─ Use Weaviate or Qdrant (full control)
   │
   └─ Self-hosted on-prem?
      └─ Use Qdrant or Milvus
```

## Key Feature: Metadata Filtering

This is critical for the **exact match problem** (Order #1766 vs #1767).

### Example: Filter by Order ID

```python
# Pinecone
results = index.query(
    vector=query_embedding,
    top_k=10,
    filter={"order_id": {"$eq": "1766"}}  # Exact match!
)

# Qdrant
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

# Weaviate
results = client.query.get("Order", ["id", "details"]).with_where({
    "path": ["order_id"],
    "operator": "Equal",
    "valueString": "1766"
}).with_near_vector({
    "vector": query_embedding
}).do()
```

## Hybrid Search Integration

Modern vector databases support **hybrid indexing**:

```python
# Qdrant example with sparse (keyword) + dense (embedding) vectors
from qdrant_client.models import SparseByteVector, PointStruct

client.upsert(
    collection_name="orders",
    points=[
        PointStruct(
            id=1,
            vector=[0.1]*384,  # Dense embedding
            payload={
                "order_id": "1766",
                "sparse_vector": SparseByteVector(...)  # Keyword index
            }
        )
    ]
)
```

## Storage and Scalability

### Memory Requirements

For 1 million documents with 384-dim embeddings:

```
Raw embeddings: 1M × 384 × 4 bytes = 1.5 GB
HNSW overhead: ~20% = 0.3 GB
Total: ~1.8 GB in RAM

Most vector DBs keep indices in memory for speed.
```

### Distributed Scaling

For 1 billion vectors, use multiple nodes:

```
3 nodes × 300M vectors each = 1B total
Each node: 1.8 GB per 1M vectors = 540 GB RAM total
Plus SSD for persistence
```

## Recommendations for RAG

1. **Small project** (< 100K vectors)
   - Use **Chroma** or FAISS
   - Simple setup, no infrastructure needed

2. **Medium project** (100K - 10M vectors)
   - Use **Pinecone** (cloud) or **Qdrant** (self-hosted)
   - Good balance of features and simplicity

3. **Large project** (> 10M vectors)
   - Use **Qdrant**, **Milvus**, or **Weaviate**
   - Distributed, high availability

4. **For the exact match problem specifically**
   - All modern databases support metadata filtering
   - Use filtering BEFORE semantic search, or
   - Use hybrid search combining sparse + dense

## Next Steps

→ [Retrieval Methods: Hybrid Search](../03-retrieval/hybrid-search.md) - Combining semantic + keyword search to solve the Order #1766 problem

→ [The Exact Match Problem](../04-exact-match/index.md) - Deep dive into solutions

--8<-- "_abbreviations.md"
