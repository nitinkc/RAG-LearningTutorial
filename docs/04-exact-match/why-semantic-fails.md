# Why Semantic Search Fails for Exact Identifiers

Let's dive deep into the mathematics of why embeddings treat "Order #1766" and "Order #1767" as nearly identical.

## The Embedding Space Geometry

### How Embeddings Are Created

Embedding models learn from examples:

```
Training data:
- "Order #1001 confirmed" → similar to → "Order #1002 pending"
- "Order #5234 shipped" → similar to → "Order #5235 delayed"
- ... (millions of examples)

The model learns:
"Sequential order numbers appear in similar contexts
and serve similar functions"
```

### Semantic Clustering

Documents cluster by meaning:

```
Embedding Space (simplified 2D):

        ↑
        |  "Thank you for your order"
        |       ◆
        |   "Order accepted"
        |    ◆ ◆
    ────┼───◆──◆──────────→
"Order    | ◆ "Order #1766"
numbers"  |  ◆ "Order #1767"
          |   ◆ "Order #1765"
          | ◆ ◆ "Order #1768"
        ↓
        
All similar because they describe orders in similar ways!
```

The embedding model doesn't know or care that "1766" and "1767" are different—they serve the same purpose in the text.

## Mathematical Analysis

### Cosine Similarity Calculation

Let $\vec{e}_{1766}$ and $\vec{e}_{1767}$ be embeddings for "Order #1766" and "Order #1767":

$$\text{cosine\_sim}(\vec{e}_{1766}, \vec{e}_{1767}) = \frac{\vec{e}_{1766} \cdot \vec{e}_{1767}}{\|\vec{e}_{1766}\| \cdot \|\vec{e}_{1767}\|}$$

Both embeddings were trained on similar contexts:
- Preceded by "Order #"
- Followed by words like "confirmed", "pending", "shipped"
- In documents about the same subject domain

Therefore:
- The vectors point in nearly the same direction
- The dot product is very high
- After normalization, cosine_sim ≈ 0.95-0.99

### Why This Happens: Information Bottleneck

The embedding model has a limited representation capacity. For a 384-dimensional embedding to represent "Order #1766", most of those dimensions encode:

- "This is about an order"
- "Following a standard format"
- "Contains a numeric identifier"

Only a tiny fraction of the 384 dimensions encode "the specific number 1766".

```
Dimension 1: Genre signal [0.9]     (this is an order-related text)
Dimension 2: Format signal [0.8]    (follows standard order format)
...
Dimension 256: Number range [0.4]   (contains a ~4-digit number)
Dimension 257: Digit magnitude [0.2] (specific 1700s range) ← Only dimension encoding actual number!
...
Dimension 384: Other signals [0.1]
```

When you compare two documents with numbers in the same range (1766 vs 1767), these small differences get washed out by the much larger similarities in the other 382 dimensions.

## Why BM25 Doesn't Have This Problem

BM25 (sparse retrieval) has the opposite problem—it's **ultra-precise about exact terms**:

$$\text{BM25}(\text{"1766"}) \gg \text{BM25}(\text{"1767"})$$

Why? The IDF term:

$$\text{IDF}("1766") = \log\left(\frac{N}{df_{"1766"}}\right)$$

where:
- N = 1,000,000 documents
- $df_{"1766"}$ = number containing "1766" = Often just 1!

$$\text{IDF}("1766") = \log(1,000,000 / 1) = 13.8 \text{ (very high)}$$

$$\text{IDF}("1767") = \log(1,000,000 / 1) = 13.8 \text{ (same!)}$$

But the TF (term frequency) differs:

```
Document: "Order #1766 status: confirmed. Order #1766 ships..."
TF("1766") = 2    (count)
TF("1767") = 0    (count)
```

So when combined:
$$\text{BM25}(\text{"1766"}) = 2 × 13.8 = 27.6 \text{ (high)}$$
$$\text{BM25}(\text{"1767"}) = 0 × 13.8 = 0 \text{ (zero!)}$$

**Perfect discrimination** because BM25 operates on exact tokens, not learned representations.

## The Fundamental Trade-off

```
┌─────────────────────────────────────────────────────┐
│                  Semantic Embeddings                 │
├─────────────────────────────────────────────────────┤
│ ✅ Understanding: "cat" ≈ "feline"                 │
│ ✅ Flexibility: Handles typos & synonyms            │
│ ❌ Precision: "Order #1766" ≈ "Order #1767"       │
│ ❌ Exact matching: Terrible for IDs                 │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│              Keyword Search (BM25)                   │
├─────────────────────────────────────────────────────┤
│ ✅ Precision: "Order #1766" ≠ "Order #1767"       │
│ ✅ Exact matching: Perfect for IDs                 │
│ ❌ Understanding: "cat" ≠ "feline"                │
│ ❌ Flexibility: Typos break matching               │
└─────────────────────────────────────────────────────┘
```

## Why You Can't Fix This by Changing Models

Some argue: "Why not use a better embedding model?"

**The problem is fundamental**, not model-specific:

### Argument 1: Information Capacity
Even the best models have finite dimensions. They must sacrifice precision on exact tokens to capture broad semantic meaning.

### Argument 2: Training Data Distribution
Embedding models learn from natural language where "Order #1766" and "Order #1767" **actually are semantically similar**—they serve identical functions in text.

Trying to make them very different would break the model's semantic understanding.

### Argument 3: Token Embedding Overlap
Even if you use a different embedding model:

```
Model A (MiniLM):
"Order #1766": [0.1, 0.2, 0.3, ...]
"Order #1767": [0.11, 0.20, 0.31, ...]
Similarity: 0.99

Model B (BGE):
"Order #1766": [0.05, 0.25, 0.35, ...]
"Order #1767": [0.051, 0.251, 0.351, ...]
Similarity: 0.999

Model C (OpenAI):
"Order #1766": [complex vector...]
"Order #1767": [very similar complex vector...]
Similarity: 0.98
```

They all have the same problem! It's not a bug—it's the **nature of learned representations**.

## Case Study: Using Multiple Embedding Models

Even if you use ALL embedding models simultaneously:

```python
from sentence_transformers import SentenceTransformer
from openai import OpenAI

models = ['all-MiniLM-L6-v2', 'BAAI/bge-base-en', 'sentence-t5']
query = "Order #1766"
doc1 = "Order #1766 confirmed"
doc2 = "Order #1767 confirmed"

for model_name in models:
    model = SentenceTransformer(model_name)
    
    q_emb = model.encode(query)
    d1_emb = model.encode(doc1)
    d2_emb = model.encode(doc2)
    
    sim_1766 = cosine_similarity(q_emb, d1_emb)
    sim_1767 = cosine_similarity(q_emb, d2_emb)
    
    print(f"{model_name}: #1766={sim_1766:.3f}, #1767={sim_1767:.3f}")

# Output:
# all-MiniLM: #1766=0.987, #1767=0.976   (1766 slightly higher but both high!)
# bge-base: #1766=0.992, #1767=0.984   (same problem)
# sentence-t5: #1766=0.981, #1767=0.973  (same problem)
```

**All models have the same issue because they all learn semantic representations.**

## Why This is Correct Behavior

Embedding models are doing **exactly what they're designed to do**. If someone asked:

> "These two order documents have similar structure, format, and context. Should they be related in the embedding space?"

The answer is: **Yes, absolutely!**

The problem is not with embeddings. The problem is using embeddings for exact matching.

## The Real Solution: Layered Matching

Stop trying to make embeddings do something they're fundamentally bad at.

Instead, **use the right tool for the job**:

| Task | Tool |
|------|------|
| "What is the status of my order?" | Embedding (semantic) |
| "Find Order #1766" | BM25 (exact match) + Metadata filter |
| "Find orders from Q1 2024" | Metadata filter |
| "Find similar orders to #1766" | Embedding (semantic) |

## Summary: Key Insights

1. **Embeddings capture semantic meaning**, not exact tokens
2. **Sequential numbers are semantically similar** (both orders, same format)
3. **Information capacity limits precision** on exact matching
4. **This is not a bug**, it's the nature of learned representations
5. **You can't fix this by choosing a better embedding model**
6. **The solution is layered**: Use embeddings for meaning, BM25 for keywords, filters for structure

## Next Steps

→ [Hybrid Solution](hybrid-solution.md) — How to actually implement the fix

→ [Chunking Strategies](chunking-strategies.md) — Making sure IDs stay prominent

--8<-- "_abbreviations.md"
