# Retrieval Methods: Dense, Sparse, and Hybrid

Now that you understand embeddings and similarity search, let's learn the different **retrieval strategies**.

The right retrieval method depends on your use case:

- **Dense retrieval** (semantic): Great for meaning, terrible for exact matches
- **Sparse retrieval** (keyword/BM25): Great for exact matches, misses synonyms
- **Hybrid retrieval**: The best of both worlds

## Topics

- [Dense Retrieval](dense-retrieval.md) — Embedding-based semantic search
- [Sparse Retrieval](sparse-retrieval.md) — BM25, TF-IDF keyword search
- [Hybrid Search](hybrid-search.md) — Combining both (your solution!)
- [Metadata Filtering](metadata-filtering.md) — Structured filters
- [Re-ranking](reranking.md) — Improving result quality

## The Core Problem (Reminder)

```
User searches: "Order #1766"

Dense (Semantic) Result:
├─ Order #1766 (0.98 similarity) ✅
├─ Order #1767 (0.96 similarity) ❌ WRONG!
└─ Order #1765 (0.95 similarity) ❌ WRONG!

Sparse (Keyword) Result:
└─ Order #1766 (exact match) ✅

Hybrid Result (Dense + Sparse):
└─ Order #1766 (highest combined score) ✅
```

## The Solution Path

You've learned:

1. ✅ Embeddings capture semantic meaning
2. ✅ But treat Order #1766 and #1767 as similar
3. ✅ BM25 captures exact keyword matches
4. ❓ How to combine them?

This section answers that question with practical solutions.

## Reading Order

1. [Dense Retrieval](dense-retrieval.md) — Recap of embeddings + search
2. [Sparse Retrieval](sparse-retrieval.md) — How BM25 works and why it finds exact matches
3. **[Hybrid Search](hybrid-search.md)** ← Start here if you want the solution
4. [Metadata Filtering](metadata-filtering.md) — Additional safety layer
5. [Re-ranking](reranking.md) — Improving results with cross-encoders

---

**Key Insight**: The best RAG systems use **all three**:

1. Dense search (find semantically similar)
2. Sparse search (find exact keywords)
3. Metadata filtering (enforce hard constraints)
