# Embedding Models: From Word2Vec to Sentence Transformers

Not all embedding models are created equal. This section traces the evolution and explains the trade-offs.

## Word2Vec (2013): The Beginning

**Word2Vec** was a breakthrough: train a simple neural network to predict nearby words, and use the hidden layer weights as embeddings.

### The Skip-gram Model

Given a word, predict surrounding words:

```
Input: "cat"
Target neighbors: "the", "sat", "on"
```

By training on billions of words, the model learns that:
- "King" and "Queen" should have similar hidden states (appear in similar contexts)
- "Good" and "Bad" should be far apart
- "Paris" - "France" + "Germany" ≈ "Berlin"

### Limitations

- Single embedding per word (no context sensitivity)
- "Bank" (river) and "Bank" (financial) get the same embedding
- Trained only on small context windows

### Code Example

```python
# Using gensim (pre-trained Word2Vec)
from gensim.models import KeyedVectors

# Load pre-trained model
model = KeyedVectors.load_word2vec_format('word2vec.bin', binary=True)

# Get embedding for a word
embedding = model['king']
print(embedding.shape)  # (300,)

# Find similar words
similar = model.most_similar('king')
# [('queen', 0.9), ('prince', 0.87), ...]

# Perform analogy
result = model.most_similar(positive=['king', 'woman'], negative=['man'])
# Returns something like 'queen'
```

## GloVe (2014): Combining Frequency & Semantics

**GloVe** (Global Vectors) improves on Word2Vec by explicitly incorporating **global word frequency statistics**.

The key insight: Word frequency and contextual similarity together form meaning.

$$J = \sum_{i,j=1}^{V} f(X_{ij}) (w_i^T \tilde{w}_j + b_i + \tilde{b}_j - \log X_{ij})^2$$

where $X_{ij}$ is the frequency of word $i$ appearing near word $j$.

- Words that co-occur frequently should have similar embeddings
- Common words (like "the") are downweighted by function $f$

### Properties

- Better than Word2Vec at capturing global patterns
- Still single embedding per word
- Performed very well on benchmarks (2014-2018 era)

## BERT and Contextual Embeddings (2018)

**BERT** introduced **context-dependent embeddings**: the same word gets different vectors depending on surrounding context.

### Why This Matters

```
"The bank approved my loan" → "bank" embedding A
"I sat on the bank of the river" → "bank" embedding B
```

BERT produces different embeddings for the same word based on context!

### How BERT Works (Simplified)

1. Break text into tokens (subword pieces)
2. Use a transformer neural network with attention layers
3. Output: one embedding per token that incorporates context

```python
from transformers import AutoTokenizer, AutoModel
import torch

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

text = "The bank is on the river."
inputs = tokenizer(text, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)

# outputs.last_hidden_state shape: (1, sequence_length, 768)
# Each word has a 768-dimensional context-aware embedding
word_embeddings = outputs.last_hidden_state[0]
```

### Challenge: Which Token to Use?

For a full document, we need one vector, not one per token.

**Options**:
1. Use the special `[CLS]` token (designed for classification)
2. Average all token embeddings
3. Use max pooling

This gets messy for document-level tasks.

## Sentence Transformers (2019): Purpose-Built for RAG

**Sentence-BERT (SBERT)** adds a pooling layer specifically for creating sentence/document embeddings:

```
Input: "This is a sentence."
    ↓
[Tokenize]
    ↓
[BERT encoder: transformer layers with attention]
    ↓
[Token embeddings from BERT: 8 vectors of 768-dim each]
    ↓
[Mean pooling: average the 8 vectors]
    ↓
Output: Single 768-dimensional sentence embedding
```

This is **perfect for RAG** because:
- One embedding per document/paragraph
- Trained on sentence/semantic similarity tasks
- Fast to compute

### Popular Models

| Model | Dimensions | Performance | Speed |
|-------|-----------|-------------|-------|
| `all-MiniLM-L6-v2` | 384 | 96.3 (benchmark) | ⚡⚡⚡ Fast |
| `all-mpnet-base-v2` | 768 | 97.8 | ⚡⚡ Medium |
| `paraphrase-MiniLM-L6-v2` | 384 | Good | ⚡⚡⚡ Fast |
| `multi-qa-MiniLM-L6-cos-v1` | 384 | Great for Q&A | ⚡⚡⚡ Fast |

### Code Example

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

documents = [
    "The quick brown fox jumps over the lazy dog",
    "A fast auburn fox leaps above a sleepy hound",
    "Python is a programming language"
]

embeddings = model.encode(documents)
print(embeddings.shape)  # (3, 384)

# Compute similarity between docs 1 and 2
similarity = embeddings[0] @ embeddings[1] / (
    np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
)
print(f"Similarity: {similarity:.3f}")  # 0.89
```

## Modern Approaches: BGE, E5, and Beyond

Recent models push performance further:

### BGE (BAAI General Embedding)
- Originally from Alibaba
- Excellent multilingual support
- Larger variants (768-1024 dims) for better quality
- Good balance of speed and quality

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('BAAI/bge-base-en-v1.5')  # 768-dim
embedding = model.encode("Query text")
```

### E5 (Entailment, Embeddings, Expansion)
- Multilingual by design
- Trained on diverse tasks
- Very strong performance on benchmarks

```python
model = SentenceTransformer('intfloat/e5-base')
```

### OpenAI's text-embedding Models
- `text-embedding-3-small` (512 dims, very strong)
- `text-embedding-3-large` (3072 dims, state-of-art)
- **Cost**: $0.02 per 1M tokens
- **Benefit**: Highest quality, OpenAI's latest research

## Comparison Table

| Model | Year | Dims | Quality | Speed | Cost | Notes |
|-------|------|------|---------|-------|------|-------|
| Word2Vec | 2013 | 300 | Basic | Fast | Free | No context |
| GloVe | 2014 | 300 | Good | Fast | Free | No context |
| BERT | 2018 | 768 | Good | Slow | Free | Context-aware, needs pooling |
| SBERT | 2019 | 384-768 | Excellent | Fast | Free | **Best for RAG** |
| BGE | 2023 | 768 | Excellent | Fast | Free | Strong multilingual |
| OpenAI | 2024 | 512-3072 | State-of-art | Medium | $$ | Best quality |

## How to Choose a Model for Your RAG

**Decision Tree**:

```
Do you have budget and care about best quality?
├─ YES → Use OpenAI text-embedding-3-small or -large
└─ NO  → 
    Is speed critical (need <10ms)?
    ├─ YES → Use all-MiniLM-L6-v2 (384-dim)
    └─ NO  →
        Do you need multilingual support?
        ├─ YES → Use BGE or E5
        └─ NO  → Use all-mpnet-base-v2 (768-dim)
```

## Code: Comparing Embedding Models

```python
from sentence_transformers import SentenceTransformer
import numpy as np
import time

models = {
    'MiniLM': 'all-MiniLM-L6-v2',
    'MPN': 'all-mpnet-base-v2',
    'BGE': 'BAAI/bge-base-en-v1.5'
}

text = "The quick brown fox jumps over the lazy dog"

for name, model_id in models.items():
    model = SentenceTransformer(model_id)
    
    start = time.time()
    emb = model.encode(text)
    elapsed = time.time() - start
    
    print(f"{name:10} | Dims: {len(emb):4} | Time: {elapsed*1000:.1f}ms")
```

**Output**:
```
MiniLM     | Dims:  384 | Time: 45.2ms
MPN        | Dims:  768 | Time: 142.3ms
BGE        | Dims:  768 | Time: 158.7ms
```

## Important Limitation (for RAG)

**All neural embedding models capture semantic similarity, not exact match**:

- Order #1766 and Order #1767 are similar in embedding space
- Customer names "John" and "Joan" are similar
- Product SKU "SKU-001A" and "SKU-001B" are similar

**This is the core problem RAG systems must solve with hybrid search!**

## Summary

| Model Family | Key Innovation | Trade-off |
|--------------|----------------|-----------|
| Word2Vec | Simple, effective | No context |
| GloVe | Frequency + context | No context |
| BERT | Context-aware | Complex pooling needed |
| SBERT | Sentence-level pooling | Still semantic only |
| BGE/E5 | Modern, multilingual | Need to download |
| OpenAI | Best quality | Cost per API call |

## Next Steps

Now that you understand embeddings, let's learn how to search with them:

→ [Distance Metrics](../02-similarity-search/distance-metrics.md)

→ [Exact vs Approximate Search](../02-similarity-search/exact-vs-ann.md)

--8<-- "_abbreviations.md"
