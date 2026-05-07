# Exact vs Approximate Search: Speed vs Accuracy

Imagine you have 10 million document embeddings. A user asks a question. You need to find the top 10 most similar documents **in under 100 milliseconds**.

**Exact search** (brute force) would compute similarity to all 10 million, then sort. This takes seconds.

**Approximate search** uses clever indexing to skip most documents and still find similar ones. This takes milliseconds.

This section explains the trade-off.

## Exact Search: Brute Force

### Algorithm

```
For each query embedding:
    1. Compute similarity to ALL document embeddings
    2. Sort by similarity
    3. Return top-K results
```

### Complexity

- **Time**: $O(n \cdot d)$ where $n$ = documents, $d$ = dimensions
- **Space**: $O(n \cdot d)$ to store all embeddings

### Example: 1 Million Documents

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# 1 million documents, 384 dimensions
embeddings = np.random.randn(1_000_000, 384)
embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

# 1 query
query = np.random.randn(1, 384)
query = query / np.linalg.norm(query)

# Exact search: compute all similarities
import time
start = time.time()
similarities = cosine_similarity(query, embeddings)
elapsed = time.time() - start

print(f"Time: {elapsed:.2f}s")  # ~2-3 seconds (slow!)
```

### Pros

✅ **Always finds the true nearest neighbors** (100% recall)

### Cons

❌ **Slow**: Seconds for millions of vectors  
❌ **Doesn't scale**: 1 billion vectors = minutes  
❌ **Wasteful**: Computes similarity even for obviously dissimilar vectors

## Approximate Search: Nearest Neighbor Graphs (HNSW)

Instead of checking all documents, we use a clever graph structure to navigate to similar vectors.

Think of it like a navigation system:

1. Start at a random point
2. Ask neighbors "who is closest to my query?"
3. Move toward the closest neighbor
4. Repeat until no improvement

### How HNSW Works (Hierarchical Navigable Small World)

**Key Idea**: Build a graph where nearby vectors are connected. Start at a high-level overview, then zoom in.

```
Level 2 (Overview):       ● ──────── ●
                         /            \
Level 1 (Medium):     ● ─── ● ─── ● ─── ●
                     /     / \     \     \
Level 0 (Detailed): ● ─── ● ─── ● ─── ● ─── ●
                    |   |   |   |   |   |   |
                    (All vectors)
```

**Algorithm**:

```
1. Start at top level
2. Visit nearby neighbors, greedily move closer to query
3. When no improvement, drop to lower level
4. Repeat until Level 0
5. Collect K-nearest from Level 0
```

### Complexity

- **Time**: $O(\log n)$ to $O(\log n + k)$ for K neighbors (vs $O(n)$ for brute force!)
- **Space**: $O(n)$ with small constant factor
- **Build time**: $O(n \log n)$ to construct graph

### Example: 1 Million Documents

```python
import faiss
import numpy as np
import time

# Create embeddings
embeddings = np.random.randn(1_000_000, 384).astype('float32')

# Build HNSW index
index = faiss.IndexHNSWFlat(384, 32)  # 32 = degree parameter
index.add(embeddings)

# Query
query = np.random.randn(1, 384).astype('float32')

# Approximate search
start = time.time()
distances, indices = index.search(query, k=10)
elapsed = time.time() - start

print(f"Time: {elapsed*1000:.2f}ms")  # ~10-50ms (fast!)
print(f"Top 10 indices: {indices[0]}")
```

### Pros

✅ **Fast**: Milliseconds for millions  
✅ **Scalable**: Works for billions  
✅ **Tunable**: Trade recall for speed

### Cons

❌ **Approximate**: Might miss some true neighbors (85-95% recall typical)  
❌ **Memory overhead**: ~10-20% extra memory for graph structure  
❌ **Parameter tuning**: Need to set M (connectivity) and ef_construction

## Other ANN Algorithms

### IVF (Inverted File) with Product Quantization

**Idea**: Divide vectors into clusters, then search within relevant clusters.

```
1. Cluster vectors into K clusters (e.g., K=100)
2. For each cluster, store compressed (quantized) vectors
3. Query:
   a. Find closest clusters
   b. Search only within those clusters
```

### Pros

✅ Small memory footprint (good compression)  
✅ Fast indexing

### Cons

❌ Slower than HNSW for high recall  
❌ More complex to tune

### Locality Sensitive Hashing (LSH)

**Idea**: Hash similar vectors to the same bucket.

### Pros

✅ Very simple  
✅ Provable guarantees

### Cons

❌ Requires many hash functions  
❌ Slower than HNSW in practice

## Comparison: Algorithms

| Algorithm | Speed | Memory | Recall | Complexity | Best For |
|-----------|-------|--------|--------|-----------|----------|
| **Brute Force** | 🐢 Slow | High | ✅ 100% | O(n) | Small datasets |
| **HNSW** | 🚀 Fast | Medium | ⚠ 90-95% | O(log n) | **Most RAG systems** |
| **IVF** | 🚄 Medium | 🔥 Low | ⚠ 80-90% | O(log n) | Large datasets |
| **LSH** | 🚄 Medium | Medium | ⚠ Variable | O(log n) | Text search |

## Recall vs Latency Trade-off

You can tune HNSW to find more neighbors (higher recall) but it takes longer:

```python
index = faiss.IndexHNSWFlat(384, M=32)
index.hnsw.ef_construction = 200  # Higher = better graph, slower build
index.hnsw.ef = 20  # Higher = more search candidates, slower search

# ef=20: fast but might miss neighbors
# ef=100: slower but finds more neighbors
# ef=200: very slow but almost as good as brute force
```

For RAG:
- **Real-time search**: ef=20-40 (~10-50ms)
- **Batch search**: ef=100-200 (~50-100ms)

## Recall-Latency Trade-off Visualization

```
100%  ╱─── Brute Force (100% recall)
Recall├   ╱
   95%│  ╱ HNSW with high ef
      │ ╱
   90%├────── HNSW (typical)
      │╱
   80%├──────────── IVF
      └──────────────────────────────
      1ms  10ms  100ms  1s
           Latency (log scale)
```

## Code: Comparing Speed

```python
import numpy as np
import faiss
import time

n_docs = 1_000_000
d = 384
k = 10

# Create test data
embeddings = np.random.randn(n_docs, d).astype('float32')
queries = np.random.randn(100, d).astype('float32')

# Method 1: Brute Force
index_bf = faiss.IndexFlatL2(d)
index_bf.add(embeddings)

start = time.time()
_, _ = index_bf.search(queries, k)
time_bf = time.time() - start

# Method 2: HNSW
index_hnsw = faiss.IndexHNSWFlat(d, 32)
index_hnsw.add(embeddings)

start = time.time()
_, _ = index_hnsw.search(queries, k)
time_hnsw = time.time() - start

print(f"Brute Force: {time_bf:.2f}s")
print(f"HNSW: {time_hnsw*1000:.2f}ms")
print(f"Speedup: {time_bf / time_hnsw:.0f}x")
```

**Typical output**:
```
Brute Force: 12.34s
HNSW: 0.058s
Speedup: 212x
```

## Recommendation for RAG

For **most RAG systems**:

```
├─ < 100K documents
│  └─ Use: Brute force (simple, exact)
│
├─ 100K - 10M documents
│  └─ Use: HNSW (best balance)
│
└─ > 10M documents
   ├─ Use: HNSW with multiple replicas (sharding)
   └─ Or: IVF with reranking
```

## Next Steps

→ [Vector Databases](vector-databases.md) - Production systems that use these algorithms

→ [Hybrid Search](../03-retrieval/hybrid-search.md) - Combining semantic with keyword search

---

**Key Takeaway**: HNSW is the standard for ANN in RAG. It trades ~5% recall for 100x+ speed. For most use cases, this is the right trade-off.

--8<-- "_abbreviations.md"
