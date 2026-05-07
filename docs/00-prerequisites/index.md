# Prerequisites: Mathematical Foundations

Before diving into RAG systems and embeddings, you need to understand the mathematical building blocks that underpin everything. If you already know linear algebra and distance metrics well, you can skip to [Embeddings](../01-embeddings/index.md).

This section covers:

1. **Vectors** (what they are, operations on them)
2. **Dot products** (the foundation of similarity)
3. **Norms and normalization** (making fair comparisons)
4. **Distance metrics** (how we measure similarity in high-dimensional spaces)

## Why This Matters

Every embedding is a vector. Every "find similar documents" operation is a distance computation. 
Understanding these operations deeply explains why RAG systems work and why they sometimes fail 
(like with Order #1766 vs #1767).

## What You Need Before This

- Comfort with basic algebra (multiplication, exponents)
- Knowing what a function is
- Basic Python (for the code examples)

## Reading Order

1. **[Linear Algebra Essentials](linear-algebra.md)** — Vectors, operations, intuition
2. **[Probability & Statistics](probability-stats.md)** — Distributions, TF-IDF foundations
3. Then continue to **[Embeddings](../01-embeddings/index.md)**

---

💡 **Tip**: Don't rush through the math. The clearer your foundation here, the more intuition you'll have when vectors get high-dimensional (hundreds or thousands of dimensions) later.

--8<-- "_abbreviations.md"
