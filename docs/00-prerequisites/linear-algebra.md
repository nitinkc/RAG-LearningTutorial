# Linear Algebra Essentials

## Vectors: The Building Block

A **vector** is an ordered list of numbers. In RAG systems, every piece of text is converted into a vector—these are called **embeddings**.

### Vector Representation

A vector $\vec{v}$ with $n$ dimensions:

$$\vec{v} = \begin{bmatrix} v_1 \\ v_2 \\ v_3 \\ \vdots \\ v_n \end{bmatrix}$$

**Example**: A 3-dimensional vector representing a point in space:

$$\vec{v} = \begin{bmatrix} 2 \\ 3 \\ 1 \end{bmatrix}$$

In Python:
```python
import numpy as np
v = np.array([2, 3, 1])
print(v.shape)  # (3,)
```

### Vector Operations

#### Addition
Vectors add element-wise:

$$\vec{u} + \vec{v} = \begin{bmatrix} u_1 + v_1 \\ u_2 + v_2 \\ \vdots \\ u_n + v_n \end{bmatrix}$$

**Example**:
$$\begin{bmatrix} 1 \\ 2 \end{bmatrix} + \begin{bmatrix} 3 \\ 4 \end{bmatrix} = \begin{bmatrix} 4 \\ 6 \end{bmatrix}$$

```python
u = np.array([1, 2])
v = np.array([3, 4])
result = u + v  # [4, 6]
```

#### Scalar Multiplication
Multiply each element by a scalar (single number):

$$c \cdot \vec{v} = \begin{bmatrix} c \cdot v_1 \\ c \cdot v_2 \\ \vdots \\ c \cdot v_n \end{bmatrix}$$

**Example**:
$$2 \cdot \begin{bmatrix} 1 \\ 3 \end{bmatrix} = \begin{bmatrix} 2 \\ 6 \end{bmatrix}$$

```python
v = np.array([1, 3])
result = 2 * v  # [2, 6]
```

## The Dot Product: The Heart of Similarity

The **dot product** (also called **inner product**) is THE fundamental operation for finding similarity between vectors.

### Definition

For vectors $\vec{u}$ and $\vec{v}$ of length $n$:

$$\vec{u} \cdot \vec{v} = u_1 v_1 + u_2 v_2 + u_3 v_3 + \cdots + u_n v_n = \sum_{i=1}^{n} u_i v_i$$

### Why It Measures Similarity

The dot product is **large and positive** when vectors point in the same direction (similar).

The dot product is **small or negative** when vectors point in different directions (dissimilar).

### Example

$$\vec{u} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \quad \vec{v} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$$

$$\vec{u} \cdot \vec{v} = (1)(1) + (0)(0) = 1 \quad \text{(same direction, maximum similarity)}$$

$$\vec{u} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \quad \vec{w} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$$

$$\vec{u} \cdot \vec{w} = (1)(0) + (0)(1) = 0 \quad \text{(perpendicular, no similarity)}$$

```python
u = np.array([1, 0])
v = np.array([1, 0])
dot_product = np.dot(u, v)  # 1

w = np.array([0, 1])
dot_product_2 = np.dot(u, w)  # 0
```

## Magnitude (Norm) of a Vector

The **magnitude** or **norm** of a vector $\vec{v}$ is its length:

$$\|\vec{v}\| = \sqrt{v_1^2 + v_2^2 + v_3^2 + \cdots + v_n^2} = \sqrt{\sum_{i=1}^{n} v_i^2}$$

This is also called the **L2 norm** or **Euclidean norm**.

### Example

$$\vec{v} = \begin{bmatrix} 3 \\ 4 \end{bmatrix}$$

$$\|\vec{v}\| = \sqrt{3^2 + 4^2} = \sqrt{9 + 16} = \sqrt{25} = 5$$

```python
v = np.array([3, 4])
magnitude = np.linalg.norm(v)  # 5.0
```

## Normalization: The Key to Fair Comparison

Here's a critical insight: **the dot product alone doesn't measure similarity fairly** if vectors have different magnitudes.

For example, a long vector pointing in a similar direction as a short vector will have a larger dot product, even though they point the same direction.

**Solution**: **Normalize** vectors to unit length (magnitude = 1):

$$\hat{\vec{v}} = \frac{\vec{v}}{\|\vec{v}\|} = \frac{1}{\|\vec{v}\|} \vec{v}$$

This gives us the **unit vector**, which points in the same direction but has length 1.

### Example

$$\vec{v} = \begin{bmatrix} 3 \\ 4 \end{bmatrix}, \quad \|\vec{v}\| = 5$$

$$\hat{\vec{v}} = \frac{1}{5} \begin{bmatrix} 3 \\ 4 \end{bmatrix} = \begin{bmatrix} 0.6 \\ 0.8 \end{bmatrix}$$

Verify: $\|\hat{\vec{v}}\| = \sqrt{0.6^2 + 0.8^2} = \sqrt{0.36 + 0.64} = \sqrt{1} = 1$ ✓

```python
v = np.array([3, 4])
v_normalized = v / np.linalg.norm(v)  # [0.6, 0.8]
print(np.linalg.norm(v_normalized))  # 1.0
```

## Cosine Similarity: The Standard for Embeddings

When vectors are normalized, the dot product has a special name and property:

$$\text{cosine\_similarity}(\vec{u}, \vec{v}) = \hat{\vec{u}} \cdot \hat{\vec{v}} = \frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\| \cdot \|\vec{v}\|}$$

Why "cosine"? Because it equals the **cosine of the angle** between the vectors:

$$\cos(\theta) = \frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\| \cdot \|\vec{v}\|}$$

where $\theta$ is the angle between them.

### Properties
- **Range**: $[-1, 1]$
- **1**: vectors point exactly the same direction (identical)
- **0**: vectors are perpendicular (unrelated)
- **-1**: vectors point opposite directions (opposite meaning)

### Example

$$\vec{u} = \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}, \quad \vec{v} = \begin{bmatrix} 1 \\ 1 \\ 0 \end{bmatrix}$$

$$\vec{u} \cdot \vec{v} = 1, \quad \|\vec{u}\| = 1, \quad \|\vec{v}\| = \sqrt{2}$$

$$\cos(\theta) = \frac{1}{1 \cdot \sqrt{2}} = \frac{1}{\sqrt{2}} \approx 0.707$$

```python
u = np.array([1, 0, 0])
v = np.array([1, 1, 0])

# Manual calculation
dot = np.dot(u, v)
norm_u = np.linalg.norm(u)
norm_v = np.linalg.norm(v)
cosine_sim = dot / (norm_u * norm_v)
print(cosine_sim)  # 0.707...

# Or use sklearn
from sklearn.metrics.pairwise import cosine_similarity
sim = cosine_similarity([u], [v])
print(sim)  # [[0.707...]]
```

## Dot Product in High Dimensions

In RAG systems, embeddings are **hundreds or thousands of dimensions** (e.g., 384-dim or 1536-dim). The dot product still works the same way mathematically, but:

- **Intuition**: Gets harder to visualize (you can't easily imagine 1536-dimensional space)
- **Computation**: Is very fast with modern hardware
- **Behavior**: In very high dimensions, random vectors are often surprisingly perpendicular and dissimilar

This is sometimes called the **curse of dimensionality**.

## Matrices: Collections of Vectors

A **matrix** is an organized collection of vectors. Each row (or column) is a vector.

$$M = \begin{bmatrix} v_1 \\ v_2 \\ v_3 \end{bmatrix} = \begin{bmatrix} m_{1,1} & m_{1,2} & m_{1,3} \\ m_{2,1} & m_{2,2} & m_{2,3} \\ m_{3,1} & m_{3,2} & m_{3,3} \end{bmatrix}$$

For example, if you have 100 text documents, each embedded into 384 dimensions, you get a **100 × 384 matrix**.

### Matrix-Vector Multiplication

Multiplying a matrix by a vector applies the dot product to each row:

$$M \vec{v} = \begin{bmatrix} \text{row}_1 \cdot \vec{v} \\ \text{row}_2 \cdot \vec{v} \\ \text{row}_3 \cdot \vec{v} \end{bmatrix}$$

This is **extremely useful for RAG**: compute the similarity of a query vector to all stored document vectors in one operation!

```python
# 100 documents, each 384-dim
documents = np.random.randn(100, 384)

# 1 query, 384-dim
query = np.random.randn(1, 384)

# Compute similarity to all documents (1 operation!)
similarities = np.dot(documents, query.T)  # Shape: (100, 1)
print(similarities.shape)
```

## Summary

| Concept | What It Is | Why It Matters |
|---------|-----------|----------------|
| Vector | Ordered list of numbers | Each embedding is a vector |
| Dot Product | $\sum u_i v_i$ | Measures similarity |
| Magnitude (Norm) | $\sqrt{\sum v_i^2}$ | Measures vector length |
| Normalization | Divide by magnitude | Makes fair comparisons |
| Cosine Similarity | Normalized dot product | Standard similarity metric in RAG |
| Matrix | Table of numbers (vectors as rows) | Efficient batch operations |

## Practice Problems

!!! question "Problem 1"
    Calculate the dot product of $\vec{u} = [2, 3]$ and $\vec{v} = [4, 1]$.
    
    **Solution**: $2 \cdot 4 + 3 \cdot 1 = 8 + 3 = 11$

!!! question "Problem 2"
    Find the magnitude of $\vec{v} = [3, 4, 12]$.
    
    **Solution**: $\|\vec{v}\| = \sqrt{9 + 16 + 144} = \sqrt{169} = 13$

!!! question "Problem 3"
    Normalize $\vec{v} = [3, 4]$.
    
    **Solution**: $\|\vec{v}\| = 5$, so $\hat{\vec{v}} = [0.6, 0.8]$

## Next Steps

Now that you understand the math, move to [Probability & Statistics](probability-stats.md) to understand TF-IDF and term importance, or jump directly to [Embeddings](../01-embeddings/index.md).
