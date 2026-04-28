# RAG Learning Tutorial - README

A comprehensive, math-first learning path for Retrieval-Augmented Generation.

## Overview

This tutorial teaches you how to build RAG systems from first principles, with emphasis on solving real-world problems like **exact identifier matching** (Order #1766 vs #1767).

**Learn:**
- Linear algebra and vector mathematics fundamentals
- How embeddings work and why they sometimes fail
- Similarity search algorithms and vector databases
- Hybrid search (combining semantic + keyword search)
- Complete RAG pipeline: ingestion → retrieval → generation
- Evaluation and production considerations

## Quick Start

### Prerequisites

- Basic Python (numpy, loops, functions)
- High school math (algebra, logarithms)
- Curiosity about how things work

You do NOT need:
- Advanced linear algebra
- PhD-level statistics
- Deep learning expertise
- Prior RAG experience

### Reading Guide

**First time learner?** Start here:

1. [index.md](docs/index.md) - Overview and learning path
2. [Prerequisites](docs/00-prerequisites/index.md) - Math foundations
3. [Embeddings](docs/01-embeddings/index.md) - How text becomes numbers
4. [Similarity Search](docs/02-similarity-search/index.md) - Finding similar documents
5. [Retrieval Methods](docs/03-retrieval/index.md) - Dense, sparse, and hybrid
6. **[The Exact Match Problem](docs/04-exact-match/index.md)** - YOUR core question
7. [RAG Pipeline](docs/05-rag-pipeline/index.md) - Full system

**Looking for specific topic?** Jump to:

- [Distance Metrics Math](docs/02-similarity-search/distance-metrics.md)
- [Why Semantic Search Fails](docs/04-exact-match/why-semantic-fails.md)
- [Hybrid Search Solution](docs/03-retrieval/hybrid-search.md)
- [Exact Match with Filtering](docs/04-exact-match/hybrid-solution.md)

## Building the Documentation Locally

### Install Dependencies

```bash
cd rag-learning-tutorial
pip install -r requirements.txt
```

### Serve Locally

```bash
python3 -m mkdocs serve
```

Then open http://localhost:8000 in your browser.

### Build Static Site

```bash
python3 -m mkdocs build
```

Output will be in `site/` directory.

## Project Structure

```
rag-learning-tutorial/
├── docs/
│   ├── index.md                    ← Start here
│   ├── 00-prerequisites/
│   │   ├── linear-algebra.md
│   │   └── probability-stats.md
│   ├── 01-embeddings/
│   │   ├─── what-are-embeddings.md
│   │   ├── embedding-models.md
│   │   └── vector-spaces.md
│   ├── 02-similarity-search/
│   │   ├── distance-metrics.md
│   │   ├── exact-vs-ann.md
│   │   └── vector-databases.md
│   ├── 03-retrieval/
│   │   ├── dense-retrieval.md
│   │   ├── sparse-retrieval.md
│   │   ├── hybrid-search.md          ← Key solution
│   │   ├── metadata-filtering.md
│   │   └── reranking.md
│   ├── 04-exact-match/
│   │   ├── index.md                 ← Your problem
│   │   ├── why-semantic-fails.md
│   │   ├── hybrid-solution.md        ← Complete solution
│   │   └── chunking-strategies.md
│   ├── 05-rag-pipeline/
│   │   ├── index.md
│   │   ├── ingestion.md
│   │   ├── retrieval-augmentation.md
│   │   ├── generation.md
│   │   └── evaluation.md
│   ├── css/
│   │   └── extra.css
│   ├── js/
│   │   ├── mathjax.js
│   │   └── theme-toggle.js
│   └── references.md
├── mkdocs.yml                      ← Site configuration
├── requirements.txt                ← Python dependencies
└── README.md                       ← This file
```

## Key Sections for Your Question

You asked about exact ID matching (Order #1766 vs #1767). Here's the path:

1. **Problem Understanding**
   - [Why Semantic Search Fails](docs/04-exact-match/why-semantic-fails.md)
   - Mathematical explanation of embedding similarity

2. **Solution Architecture**
   - [Hybrid Search](docs/03-retrieval/hybrid-search.md)
   - How to combine semantic + keyword search

3. **Complete Implementation**
   - [Hybrid Solution](docs/04-exact-match/hybrid-solution.md)
   - Step-by-step code example

4. **Supporting Strategies**
   - [Metadata Filtering](docs/03-retrieval/metadata-filtering.md)
   - [Chunking Strategies](docs/04-exact-match/chunking-strategies.md)
   - [Re-ranking](docs/03-retrieval/reranking.md)

## Mathematics Covered

This tutorial teaches:

- **Linear Algebra**: Vectors, dot products, norms, cosine similarity
- **Probability**: IDF, term frequency, TF-IDF scoring
- **Geometry**: High-dimensional space behavior, distance metrics
- **Information Retrieval**: BM25, ranking algorithms, evaluation metrics

All with intuition + derivations + code examples.

## Code Examples Included

Each topic includes practical Python code:

```python
# Embeddings
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
embedding = model.encode("Order #1766")

# Similarity search
import faiss
index = faiss.IndexHNSWFlat(384, 32)
distances, indices = index.search(query_vector, k=10)

# BM25 (keyword search)
from rank_bm25 import BM25Okapi
bm25 = BM25Okapi(corpus)
scores = bm25.get_scores(tokens)

# Hybrid combination
hybrid_score = w_dense * dense_norm + w_sparse * sparse_norm

# Vector database
from qdrant_client import QdrantClient
results = client.search(
    query_vector=embedding,
    query_filter={"order_id": "1766"}
)
```

## Recommended Tools

**For Learning**:
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) - Documentation engine used
- [Jupyter Notebooks](https://jupyter.org/) - Interactive exploration
- [Hugging Face Spaces](https://huggingface.co/spaces) - Run code without setup

**For Implementation**:
- [Qdrant](https://qdrant.tech/) - Vector database (free)
- [LangChain](https://langchain.com/) - RAG framework
- [Sentence Transformers](https://sbert.net/) - Embedding models
- [rank-bm25](https://github.com/dorianbrown/rank_bm25) - BM25 library

**For Production**:
- [Elasticsearch](https://elastic.co/) - Production search
- [Pinecone](https://pinecone.io/) - Managed vector DB
- [Weaviate](https://weaviate.io/) - Enterprise vector DB

## FAQ

### How long to complete?
- **Quick read** (focusing on your question): 4-6 hours
- **Full tutorial** (all sections): 20-30 hours
- **Implementation** (building a system): 40+ hours

### Do I need to know linear algebra?
No! Section 0 teaches everything from scratch with intuition and derivations.

### Can I skip the math?
Not recommended. The math explains WHY things work. Skipping it means you'll copy code without understanding why Order #1766 pattern fails.

### How is this different from other RAG tutorials?
1. **Math-first approach**: Explains WHY, not just HOW
2. **Problem-focused**: Built around solving the exact match problem
3. **Production-ready**: Covers real challenges (chunking, filtering, re-ranking)
4. **Complete**: Links all concepts together

### Can I use this for my production system?
Yes! The concepts and code examples are production-ready. For large scale, use Qdrant or Pinecone instead of local FAISS.

## Contributing

Found a mistake or want to add content?

1. Fork this repository
2. Create a new branch (`git checkout -b fix/issue`)
3. Make changes
4. Submit a pull request

## License

This tutorial is provided as-is for learning purposes.

## Next Steps

1. **Start reading**: Open [docs/index.md](docs/index.md#learning-path)
2. **Build locally**: `python3 -m mkdocs serve`
3. **Experiment**: Modify code examples as you learn
4. **Implement**: Build your own RAG system

---

**Happy learning!** 🚀

For questions or feedback, refer to [references.md](docs/references.md) for resources and communities.
