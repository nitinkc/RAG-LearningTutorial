# Similarity Search: Finding Relevant Documents

Now that you understand embeddings and how vector spaces work, let's learn how to **find similar documents efficiently**.

This section covers:

1. **Distance metrics** — Different ways to measure "similarity" between embeddings
2. **Exact vs Approximate search** — Brute force vs fast algorithms
3. **Vector databases** — Systems optimized for embedding search
4. **Trade-offs** — Speed vs recall, storage vs quality

## The Core Problem

Given:
- A **query embedding** (from user question)
- **Millions of document embeddings** (in a database)

Find:
- The **K most similar document embeddings** (top-K nearest neighbors)

In real-time (< 100ms ideally).

## Topics

- [Distance Metrics](distance-metrics.md) — Cosine, Euclidean, Dot Product (with full derivations)
- [Exact vs Approximate Search](exact-vs-ann.md) — Brute force vs HNSW vs IVF algorithms
- [Vector Databases](vector-databases.md) — Chroma, Pinecone, Weaviate, FAISS comparisons

## Why This Matters for RAG

- Fast retrieval = responsive user experience
- Better indexing = better recall (fewer relevant docs missed)
- Different metrics = different results (cosine vs Euclidean behave differently in your data)

## Key Insight

> For **most** RAG systems, **cosine similarity** with **HNSW indexing** is the right choice. It's fast, accurate, and well-understood.

## Reading Order

1. Start here (done!)
2. [Distance Metrics](distance-metrics.md) — Understand the math
3. [Exact vs Approximate Search](exact-vs-ann.md) — Learn how to search efficiently
4. [Vector Databases](vector-databases.md) — See production systems

Then move to [Retrieval Methods](../03-retrieval/index.md) to learn about hybrid search.

--8<-- "_abbreviations.md"
