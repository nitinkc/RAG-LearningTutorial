# Probability & Statistics Foundations

For RAG systems to work well, you need to understand **term importance** and **how to score documents**. This section builds the statistical foundations.

## Probability Basics

### What Is Probability?

A **probability** is a number between 0 and 1 representing how likely something is:

- **P(event) = 0**: The event is impossible
- **P(event) = 0.5**: The event is equally likely or unlikely
- **P(event) = 1**: The event is certain

### Conditional Probability

Given that event $A$ happened, what's the probability that event $B$ happens?

$$P(B | A) = \frac{P(A \text{ and } B)}{P(A)}$$

**Example**: In a document collection, what's the probability that a document is relevant given that it contains the word "order"?

$$P(\text{relevant} | \text{contains "order"})$$

## Information Theory: Measuring Importance

The more **surprising** a term is (appears in fewer documents), the more **informative** it is.

### Inverse Document Frequency (IDF)

The **inverse document frequency** of a term measures its importance:

$$\text{IDF}(t) = \log\left(\frac{N}{df_t}\right)$$

where:
- $N$ = total number of documents
- $df_t$ = number of documents containing term $t$

### Why Logarithm?

The logarithm compresses large ratios into manageable numbers. More importantly, **IDF grows as terms become rarer**, which is what we want:

- If a term appears in 1 document out of 1000: $\text{IDF} = \log(1000/1) = \log(1000) \approx 6.9$
- If a term appears in 500 documents out of 1000: $\text{IDF} = \log(1000/500) = \log(2) \approx 0.3$

The rare term gets a higher score!

### Example

Suppose we have 1000 documents:

| Term | Appears In | IDF |
|------|-----------|-----|
| "Order" (common) | 500 docs | $\log(1000/500) = 0.30$ |
| "transaction" (uncommon) | 50 docs | $\log(1000/50) = 2.30$ |
| "order_#1766" (very rare) | 1 doc | $\log(1000/1) = 6.91$ |

Notice: **Exact identifiers like "order_#1766" get very high IDF scores** because they're unique!

## Term Frequency: Measuring Presence

**Term Frequency (TF)** counts how often a term appears in a document:

$$\text{TF}(t, d) = \text{count of } t \text{ in document } d$$

However, longer documents naturally have higher term frequencies. We often **normalize** by document length:

$$\text{TF}_{\text{norm}}(t, d) = \frac{\text{count of } t \text{ in } d}{\text{total words in } d}$$

## TF-IDF: Combining Frequency and Importance

**TF-IDF** is the product:

$$\text{TF-IDF}(t, d) = \text{TF}(t, d) \times \text{IDF}(t)$$

This gives high scores to terms that are:
1. **Common in the document** (high TF)
2. **Rare across all documents** (high IDF)

### Example

Document: "Customer with Order #1766 made a purchase of $100. Order #1766 is confirmed."

| Term | TF | IDF | TF-IDF |
|------|----|----|--------|
| "order" | 2/13 ≈ 0.15 | 0.30 | 0.045 |
| "#1766" | 2/13 ≈ 0.15 | 6.91 | 1.04 |
| "purchase" | 1/13 ≈ 0.08 | 4.50 | 0.36 |

**The exact identifier "#1766" dominates the TF-IDF score** because it's specific and rare!

```python
from sklearn.feature_extraction.text import TfidfVectorizer

documents = [
    "Customer with Order #1766 made a purchase",
    "Order #1767 is pending verification"
]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

# Get term scores for first document
feature_names = vectorizer.get_feature_names_out()
scores = tfidf_matrix[0].toarray().flatten()

for name, score in zip(feature_names, scores):
    if score > 0:
        print(f"{name}: {score:.3f}")
```

## Why This Matters for RAG

In **sparse retrieval** (the keyword/BM25 approach), TF-IDF and similar scoring methods are how we find documents containing exact matches:

- Search for "Order #1766"?
- → Find documents with very high TF-IDF for "1766" (because it's unique)
- → Will correctly return Order #1766 documents, NOT Order #1767

This is why **BM25 search** (an improved TF-IDF variant) works well for exact matches! It's mathematically designed to prioritize rare, specific terms—exactly what order numbers are.

## Distributions and Probability Densities

When working with embeddings and vectors, we often assume they follow a **distribution**—a mathematical description of how likely different values are.

### Gaussian (Normal) Distribution

The most common distribution:

$$P(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x - \mu)^2}{2\sigma^2}\right)$$

where:
- $\mu$ = mean (center)
- $\sigma$ = standard deviation (spread)

**Why it matters**: Many embedding models produce outputs that are approximately normally distributed. This is important for understanding statistical properties of similarity scores.

```python
import numpy as np
import matplotlib.pyplot as plt

# Generate random samples from normal distribution
data = np.random.normal(loc=0, scale=1, size=10000)

plt.hist(data, bins=50)
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.title("Normal Distribution (μ=0, σ=1)")
plt.show()
```

## Summary Table

| Concept | Formula | Purpose in RAG |
|---------|---------|----------------|
| TF | count of term in doc | Measures how often a term appears |
| IDF | $\log(N / df_t)$ | Measures how rare/important a term is |
| TF-IDF | TF × IDF | Keyword similarity scoring |
| BM25 | Extended TF-IDF | Production-grade sparse search |

## Key Insight: Why Hybrid Search Works

- **Semantic search** (embeddings + cosine similarity) → captures *meaning*
- **Sparse search** (BM25/TF-IDF) → captures *exact terms*

For "Order #1766":
- Semantic search might return Order #1767 too (because they're semantically similar)
- Sparse search returns ONLY documents with "1766" in them (exact match)

**Hybrid** = both together = best of both worlds!

## Practice Problems

!!! question "Problem 1"
    If a collection has 10,000 documents and a term appears in 100 of them, what is the IDF?
    
    **Solution**: $\text{IDF} = \log(10000 / 100) = \log(100) \approx 4.61$

!!! question "Problem 2"
    A document has 200 words, and the term "customer" appears 5 times. What is the normalized TF?
    
    **Solution**: $\text{TF}_{\text{norm}} = 5 / 200 = 0.025$

!!! question "Problem 3"
    If IDF("customer") = 2.0 and $\text{TF}_{\text{norm}}$ = 0.025, what is TF-IDF?
    
    **Solution**: $\text{TF-IDF} = 0.025 \times 2.0 = 0.05$

## Next Steps

Now you have the mathematical foundations! Move to [Understanding Embeddings](../01-embeddings/index.md) to see how modern text → numbers conversion works.
