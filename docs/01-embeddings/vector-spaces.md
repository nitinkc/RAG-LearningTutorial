# Vector Spaces and High-Dimensional Geometry

When you move from 2D or 3D to hundreds of dimensions (as with embeddings), geometry behaves very differently. This section explains why, and what it means for RAG systems.

## From 2D to Many Dimensions

### 2D Space (Easy to Visualize)

```
    ↑
    |    ● Point B
    |   /
    |  /
    | /
    |●─────→
    |Point A
    +
```

Distance between points is easy to compute and visualize.

### 384-Dimensional Space (Embeddings)

We can't visualize this, but we can reason about it mathematically.

In an embedding space with $d$ dimensions, every point is described by $d$ numbers.

For sentence-BERT: $d = 384$.

## The Curse of Dimensionality

### Surprising Fact: Random Vectors Are Almost Perpendicular

In high dimensions, random vectors point in almost completely different directions!

Let's measure this: generate two random 384-dimensional vectors and compute their similarity.

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Generate random vectors
dim = 384
v1 = np.random.randn(dim)
v2 = np.random.randn(dim)

# Normalize
v1 = v1 / np.linalg.norm(v1)
v2 = v2 / np.linalg.norm(v2)

# Compute similarity
sim = np.dot(v1, v2)
print(f"Similarity: {sim:.4f}")
# Output: Something like 0.0234 (very close to 0, meaning perpendicular)
```

**Why?** In high dimensions, there's "room" in all directions, so random directions are nearly orthogonal.

### Consequence for RAG

This has important implications:

1. **Random documents are very different** (good—we can distinguish them)
2. **But "similar" documents might only be moderately close!** (0.7-0.8 similarity is actually quite close in high dimensions)
3. **Noise and minor variations are magnified**

## The Volume Paradox

Another strange property: in high dimensions, **most of the volume is on the surface**.

Consider a hypersphere (n-dimensional sphere) of radius $r$:

$$\text{Volume} = \frac{\pi^{d/2}}{\Gamma(d/2 + 1)} r^d$$

As $d$ increases, the volume becomes increasingly concentrated at the **surface** (the boundary), not at the center.

### Implication

In a RAG system with embeddings in a database:

- Points near the surface are sparsely distributed
- Real clusters of similar documents are relatively rare
- Most of the volume is "empty space"

This is why **approximate nearest neighbor (ANN) algorithms** work so well—they exploit this structure to skip most of the empty space.

## Intrinsic Dimensionality

Not all 384 dimensions are equally important!

Most real data (embeddings from documents) actually lie on a **lower-dimensional manifold** within the full 384-dimensional space.

The **intrinsic dimensionality** is much lower than 384.

### Example

Imagine 1 million documents, each with a 384-dimensional embedding. But all documents are variations on just 50 key topics. The data effectively lives in ~50 dimensions, even though represented in 384.

### Implication for RAG

- You don't need extremely high-dimensional spaces
- 384 dimensions is often more than enough
- But each extra dimension adds **computational cost**
- This is why **dimensionality reduction** techniques (PCA, autoencoders) can work

## Distance Concentration

As dimensions increase, most pairwise distances **converge to the same value**!

For random data in $d$ dimensions:

$$\text{E}[\text{distance}] \approx C \sqrt{d}$$

where $C$ is a constant.

### Visualization

```python
import numpy as np
import matplotlib.pyplot as plt

distances = []

for d in [2, 10, 50, 100, 384]:
    # Generate 100 random points
    points = np.random.randn(100, d)
    
    # Compute pairwise distances
    from scipy.spatial.distance import pdist
    dists = pdist(points)
    distances.append(dists)

# Plot distributions
for d, dists in zip([2, 10, 50, 100, 384], distances):
    plt.hist(dists, bins=30, alpha=0.5, label=f"d={d}")

plt.xlabel("Distance")
plt.ylabel("Frequency")
plt.legend()
plt.title("Pairwise Distances in Different Dimensions")
plt.show()
```

**Result**: As $d$ increases, histogram becomes narrower and more peaked—distances are more similar to each other.

### Why This Matters

- In 2D, "close" vs "far" are clearly different
- In 384D, most points are at roughly the same distance from each other
- This makes finding "nearest" neighbors harder (requires more precision)
- Reinforces why ANN algorithms are necessary

## Cosine Similarity in High Dimensions

When vectors are normalized (as embeddings typically are), we use **cosine similarity**:

$$\cos(\theta) = \vec{u} \cdot \vec{v}$$

In high dimensions with random data:

$$E[\cos(\theta)] = 0, \quad \text{but spread is large}$$

Actual similarities might range from -0.2 to 0.2, with most around 0.

**For actual document embeddings**, clus ters of related documents form clouds with mutual similarities like 0.6-0.9.

## Visualizing High-Dimensional Data

You can't plot 384 dimensions, but you can **project** to 2D or 3D:

### TSNE (t-Distributed Stochastic Neighbor Embedding)

Preserves local neighbor structure:

```python
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# embeddings shape: (1000, 384)
tsne = TSNE(n_components=2, random_state=42)
embeddings_2d = tsne.fit_transform(embeddings)

plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c=labels, cmap='viridis')
plt.title("Document Embeddings (TSNE projection)")
plt.show()
```

### UMAP (Uniform Manifold Approximation and Projection)

Faster than TSNE, also preserves structure:

```python
from umap import UMAP

umap = UMAP(n_components=2)
embeddings_2d = umap.fit_transform(embeddings)

plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c=labels)
plt.show()
```

These projections show clusters of similar documents and help debug embedding quality, but **remember**: projections lose information!

## Norms in High Dimensions

In high dimensions, **most randomly-generated vectors have similar magnitude** (norm).

$$\text{E}[\|v\|] \approx \sqrt{d}$$

For $d = 384$: $\|v\| \approx 19.6$

**Implication**: When we normalize vectors (divide by their norm), we're "leveling the playing field" so that vectors in different dimensions have equal importance.

Most embedding models output normalized vectors:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embedding = model.encode("Text")

# Most models normalize automatically
magnitude = np.linalg.norm(embedding)
print(f"Magnitude: {magnitude:.4f}")  # Should be ~1.0
```

## Practical Implications for RAG

| Property | Impact on RAG |
|----------|---------------|
| Random vectors are perpendicular | Most documents are distinguishable |
| Distance concentration | Need precise distance computation |
| Intrinsic dimensionality < 384 | Could use smaller models if needed |
| Normalized vectors have equal norm | Fair comparison between vectors |

## Summary

High-dimensional spaces are **weird**:
- Most volume is on the surface
- Random points are far apart
- Most pairwise distances are similar in magnitude
- "Close" and "far" are relative

But these properties actually make **embedding-based search work well** once you understand them.

## Next Steps

Now let's apply this knowledge:

→ [Distance Metrics](../02-similarity-search/distance-metrics.md) - Detailed math of different similarity measures

→ [Exact vs Approximate Search](../02-similarity-search/exact-vs-ann.md) - How to search among millions of vectors efficiently

--8<-- "_abbreviations.md"
