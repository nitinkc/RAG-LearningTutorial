# What Are Embeddings?

An **embedding** is a representation of text as a vector of numbers. Instead of storing text directly, we store numbers that capture its meaning.

## The Intuition

Imagine a 2D space (like a piece of paper) where:

- Words with similar meanings are placed **close to each other**
- Words with different meanings are placed **far apart**

For example:

```
        ↑ "king"
        |     ✗ "queen"
        |        ✗
        |
    ————+———→
        |    ✗ "man"
        |     ✗ "woman"
        |
   ✗ "dog"
```

**In reality**, embeddings are in very high dimensions (hundreds or thousands), but the principle is the same: nearby vectors = similar meanings.

## Concrete Example

Let's say we have three sentences:

1. "The cat sat on the mat"
2. "A feline rested on a rug"
3. "The dog chased the ball"

An embedding model might produce:

| Sentence | Embedding (384-dimensional) |
|----------|---------------------------|
| Sentence 1 | [0.12, -0.45, 0.73, ..., 0.02] |
| Sentence 2 | [0.11, -0.43, 0.71, ..., 0.03] |
| Sentence 3 | [-0.31, 0.28, -0.12, ..., 0.89] |

**Notice**:
- Sentences 1 and 2 have vectors that are very similar (they describe similar situations)
- Sentence 3 has a vector quite different (different scenario)

We can measure this with cosine similarity (from the linear algebra section):

$$\text{cosine\_similarity}(\text{Sent 1}, \text{Sent 2}) \approx 0.98 \quad \text{(very similar)}$$

$$\text{cosine\_similarity}(\text{Sent 1}, \text{Sent 3}) \approx 0.42 \quad \text{(less similar)}$$

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

sent1 = "The cat sat on the mat"
sent2 = "A feline rested on a rug"
sent3 = "The dog chased the ball"

emb1 = model.encode(sent1)
emb2 = model.encode(sent2)
emb3 = model.encode(sent3)

print(f"emb1 shape: {emb1.shape}")  # (384,)
print(f"Similarity 1-2: {np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)):.3f}")
print(f"Similarity 1-3: {np.dot(emb1, emb3) / (np.linalg.norm(emb1) * np.linalg.norm(emb3)):.3f}")
```

## Why Embeddings Capture Meaning

Neural networks are trained on massive amounts of text. During training, the network learns that:

- Words appearing in similar contexts should have similar embeddings
- "King" and "Queen" appear in similar contexts
- Therefore, their embeddings are close
- We can perform analogy: "King - Man + Woman ≈ Queen"

This is a powerful emergent property—nobody explicitly told the network to encode these relationships!

## Limitations: The Order #1766 Problem

Here's the critical issue for exact match search:

From an embedding model's perspective:
- "Order #1766" appears in contexts like "your order", "confirmed order", "order total"
- "Order #1767" appears in very similar contexts
- Therefore, the embedding treats them as nearly identical!

$$\text{cosine\_similarity}("Order #1766", "Order #1767") \approx 0.99 \quad \text{(almost the same)}$$

But they're NOT the same! They're different orders.

The embedding model is doing exactly what it's designed to do—capture semantic similarity. But for structured data like order numbers, we need different approaches. (This is solved in [The Exact Match Problem](../04-exact-match/index.md).)

## Example: What a Real Embedding Looks Like

Using a real embedding model:

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')  # 384-dimensional

text = "What is the meaning of life?"
embedding = model.encode(text)

print(f"Embedding shape: {embedding.shape}")  # (384,)
print(f"First 10 values: {embedding[:10]}")
# Output: [-0.08  0.23 -0.15  0.42  0.01 -0.09  0.67 -0.32  0.11  0.03]

print(f"Min: {embedding.min():.3f}, Max: {embedding.max():.3f}")
# Output: Min: -0.999, Max: 0.893

# Magnitude after normalization
magnitude = np.linalg.norm(embedding)
print(f"Magnitude: {magnitude:.3f}")  # Should be ~1.0 for normalized embeddings
```

## Types of Embeddings

1. **Word embeddings** (Word2Vec, GloVe): Single words → vectors
2. **Sentence embeddings** (Sentence-BERT): Entire sentences → vectors
3. **Document embeddings**: Entire documents → vectors
4. **Contextual embeddings** (BERT, GPT): Same word has different vectors in different contexts

For RAG systems, we typically use **document/passage embeddings** (short documents or chunks).

## Dimensions and Trade-offs

| Model | Dimensions | Speed | Quality | Use Case |
|-------|-----------|-------|---------|----------|
| ONNX mini models | 96 | Very Fast | Good | Real-time, resource-constrained |
| MiniLM | 384 | Fast | Very Good | Most RAG systems |
| BGE | 768 | Medium | Excellent | Production systems |
| OpenAI text-embedding-3-large | 3072 | Slow | State-of-art | When money/latency not a concern |

**Higher dimensions** = more expressive (better quality) but **slower and more storage**.

## How to Create Embeddings

### Option 1: Using Pre-trained Models (Recommended)

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
documents = [
    "This is the first document",
    "Here is the second document",
    "And the third one"
]

embeddings = model.encode(documents)
print(embeddings.shape)  # (3, 384)
```

### Option 2: Using OpenAI API

```python
from openai import OpenAI

client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Strawberry shortcake"
)

embedding = response.data[0].embedding
print(f"Embedding length: {len(embedding)}")  # 1536
```

### Option 3: Using Hugging Face Transformers

```python
from transformers import AutoTokenizer, AutoModel
import torch

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

text = "This is a sample text"
inputs = tokenizer(text, return_tensors="pt")

# Get embeddings
with torch.no_grad():
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state[:, 0, :]  # Take [CLS] token

print(embeddings.shape)
```

## Summary

| Concept | Definition |
|---------|-----------|
| **Embedding** | Vector of numbers representing text meaning |
| **Embedding dimension** | Length of vector (e.g., 384) |
| **Cosine similarity** | How similar two embeddings are (0-1) |
| **Context** | Texts with similar context get similar embeddings |
| **Limitation** | Treats "Order #1766" and "Order #1767" as similar |

## Next Steps

Ready to understand how embedding models work? → [Embedding Models](embedding-models.md)

Or skip ahead to [Distance Metrics](../02-similarity-search/distance-metrics.md) if you want to learn how to use embeddings for search.
