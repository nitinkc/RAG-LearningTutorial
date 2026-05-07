# Understanding Embeddings

An **embedding** is a conversion of text into a vector of numbers. This is the foundation of modern RAG systems.

This section explains:

1. **What embeddings are** (intuition + what they look like)
2. **How embedding models work** (from Word2Vec to modern transformers)
3. **Why embeddings capture meaning** (the geometry of language)
4. **How to choose an embedding model** (trade-offs and comparisons)

## Key Insight

> An embedding is just a vector of numbers that represents the *meaning* of a word or document. Vectors that are geometrically close to each other represent similar meanings.

## Topics Covered

- [What are Embeddings](what-are-embeddings.md) — Concrete examples and intuition
- [Embedding Models](embedding-models.md) — Word2Vec, GloVe, BERT, Sentence Transformers
- [Vector Spaces](vector-spaces.md) — High-dimensional geometry and implications

## Why Embeddings Matter for RAG

1. **Semantic search**: Find documents with similar *meaning*, not just matching keywords
2. **Speed**: Comparing vectors is fast; comparing full texts is slow
3. **Relevance**: Embeddings capture nuanced meaning that keyword search misses
4. **Cross-lingual**: Same meaning, different languages, can be close in embedding space

## But Remember...

Embeddings have limitations:

- ❌ Excellent for capturing meaning
- ❌ **Terrible for exact identifiers** (Order #1766 ≈ Order #1767 in embedding space)
- ❌ Limited by context window of embedding model
- ❌ Biases in training data are captured in embeddings

This is exactly why RAG systems need **hybrid search** (semantic + keyword). We'll revisit this in [The Exact Match Problem](../04-exact-match/index.md).

## Reading Path

**I recommend reading in order**:

1. Start here (done!)
2. [What are Embeddings](what-are-embeddings.md)
3. [Embedding Models](embedding-models.md)
4. [Vector Spaces](vector-spaces.md)

Then move to [Similarity Search](../02-similarity-search/index.md).

---

**Key Takeaway**: Embeddings are powerful but imperfect. They excel at capturing semantic meaning but fail for structured data. Understanding their strengths and weaknesses is crucial for building good RAG systems.

--8<-- "_abbreviations.md"
