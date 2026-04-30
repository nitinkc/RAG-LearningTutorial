# RAG Practical Labs: Hands-On Learning

Welcome to the Practical Labs section! These labs are designed as **college-level academic exercises** that build from fundamentals to advanced topics. Each lab combines **theory, implementation, and real-world data**.

## Lab Curriculum Overview

### 📚 Lab Structure
- **Duration**: 1-2 hours each
- **Format**: Jupyter notebooks + guided exercises
- **Difficulty**: Incremental (Foundations → Intermediate → Advanced)
- **Skills**: Python, data structures, vector math, databases, information retrieval

---

## 🧮 Lab 0: Environment Setup & Fundamentals
**Level**: Foundations | **Time**: 30 min

Set up your development environment and verify all tools are working.

**What You'll Learn:**
- Install required packages (sentence-transformers, Chroma, scikit-learn, pandas)
- Understand directory structure
- Verify GPU/CPU availability
- First steps with embeddings
- Lab workflow and best practices

**Key Concepts:**
- Python virtual environments
- Package management
- Jupyter notebooks
- Performance basics

**Deliverable**: Working environment with all libraries imported successfully

---

## 📐 Lab 1: Vector Math & Distance Metrics
**Level**: Foundations | **Time**: 1.5 hours

Build intuition for vectors before working with embeddings.

**What You'll Learn:**
- Implement vectors from scratch (no NumPy)
- Calculate dot product, magnitude, cosine similarity
- Visualize vectors in 2D and 3D
- Compare distance metrics (Euclidean, Manhattan, Cosine)
- Understand why cosine similarity matters for embeddings

**Key Concepts:**
- Vector operations (dot product, normalization)
- Distance metrics and their geometric meaning
- Similarity functions
- Computational complexity

**Real-World Application**: Why cosine similarity is preferred for embeddings (sparse data, high dimensions, angle-based matching)

**Deliverable**: 
- Working implementations of: dot product, cosine similarity, Euclidean distance
- 2D/3D vector visualization
- Distance comparison on sample vectors

---

## 🔤 Lab 2: Text Embeddings & Vector Space
**Level**: Foundations | **Time**: 1.5 hours

Learn how text becomes vectors and explore embedding space.

**What You'll Learn:**
- Use SentenceTransformer to embed text
- Explore embedding properties (dimensionality, scale, distribution)
- Compare sentence similarities using learned embeddings
- Visualize high-dimensional embeddings with t-SNE
- Understand pretrained model architecture basics

**Key Concepts:**
- Transformer-based embeddings
- Sentence-level vs token-level representations
- Embedding dimensions and their meaning
- Dimensionality reduction for visualization
- Semantic similarity discovery

**Real-World Application**: How models automatically learn to place similar texts nearby in vector space

**Deliverable**:
- Embedded corpus of sentences
- Similarity matrix visualization
- t-SNE plot showing semantic clustering
- Analysis of top-k similar sentences for queries

---

## 🗄️ Lab 3: Working with Vector Databases
**Level**: Intermediate | **Time**: 2 hours

Store, retrieve, and search vectors in a database.

**What You'll Learn:**
- Create and populate a Chroma vector database
- Understand HNSW indexing (Hierarchical Navigable Small World)
- Perform vector similarity search
- Add metadata to vectors
- Delete and update vectors
- Save and load databases

**Key Concepts:**
- Approximate Nearest Neighbor (ANN) algorithms
- HNSW index construction and search
- Database persistence
- Metadata filtering
- Basic performance characteristics

**Real-World Application**: How production systems efficiently store and search millions of vectors

**Deliverable**:
- Working Chroma database with 1000+ vectors
- Metadata-aware search queries
- Database persistence and reload
- Performance analysis (search time vs dataset size)

---

## 💾 Lab 4: Real Data Ingestion - MongoDB & Chroma
**Level**: Intermediate | **Time**: 2.5 hours

End-to-end ingestion pipeline using real open-source data.

**What You'll Learn:**
- Load MongoDB sample dataset (restaurants or movies)
- Chunk documents intelligently
- Embed chunks and store in Chroma
- Understand data flow in RAG systems
- Handle metadata preservation
- Deal with variable-length documents

**Data Source**: MongoDB Open-Source Sample Datasets
- **Restaurants**: 25K+ restaurant reviews and details
- **Movies**: 23K movies with full information
- **Twitter**: Tweet archive (alternative source)

**Key Concepts:**
- Data loading and preprocessing
- Chunking strategies (fixed-size, semantic, sliding window)
- Bulk ingestion
- Metadata mapping
- Index optimization

**Real-World Application**: Building knowledge bases from unstructured data

**Deliverable**:
- Ingested vector database with 1000+ chunks from real data
- Metadata preservation (restaurant name, location, ratings)
- Chunking strategy analysis
- Search performance on real queries

---

## 🎯 Lab 5: Exact vs Semantic Match - The Core Problem
**Level**: Intermediate | **Time**: 2 hours

Discover why semantic search fails for exact matches, then fix it.

**What You'll Learn:**
- Create a dataset with similar IDs (Order #1766 vs #1767)
- Show why semantic search fails on exact matches
- Visualize embedding similarity in 2D
- Understand the fundamental limitation
- Introduce hybrid search as the solution
- Analyze failure cases and their causes

**Key Concepts:**
- Curse of similarity in embeddings
- When embeddings aren't the right tool
- Hybrid retrieval motivation
- Trade-offs in information retrieval

**Real-World Application**: Why your RAG system might return the wrong order/record

**Deliverable**:
- Dataset demonstrating the problem
- Comparison plots showing embedding similarity
- Analysis of why numbers look "similar" to embeddings
- Understanding of when semantic search works vs fails

---

## 🔀 Lab 6: Hybrid Search Implementation
**Level**: Intermediate-Advanced | **Time**: 2.5 hours

Combine semantic and keyword search for robust retrieval.

**What You'll Learn:**
- Implement BM25 sparse retrieval
- Score documents with keyword matching
- Implement Reciprocal Rank Fusion (RRF)
- Combine dense and sparse results
- Compare hybrid vs pure semantic search
- Optimize ranking strategies
- Handle tie-breaking and result aggregation

**Key Concepts:**
- TF-IDF and BM25 scoring
- Dense vs sparse retrieval
- Result ranking and fusion
- Precision vs Recall trade-offs
- Multi-stage retrieval pipelines

**Real-World Application**: Production-ready retrieval that handles both semantic meaning and exact terms

**Deliverable**:
- Working BM25 implementation
- Hybrid search combining dense + sparse
- Performance comparison (semantic vs hybrid)
- Optimized ranking strategy
- Evaluation metrics (MRR, NDCG)

---

## 🔗 Lab 7: Complete RAG Pipeline
**Level**: Advanced | **Time**: 3 hours

Build an end-to-end RAG system with evaluation.

**What You'll Learn:**
- System architecture and data flow
- Ingestion pipeline with quality checks
- Multi-stage retrieval (dense → hybrid → rerank)
- LLM augmentation with retrieved context
- Evaluation frameworks (relevance, faithfulness, latency)
- Production considerations
- Monitoring and optimization

**Key Concepts:**
- RAG system design
- Retrieval evaluation
- Context selection strategies
- LLM prompt engineering
- Performance monitoring
- Cost-latency trade-offs

**Real-World Application**: Building a production RAG system for custom knowledge bases

**Deliverable**:
- Complete working RAG pipeline
- Evaluation metrics dashboard
- Performance analysis
- Optimization recommendations

---

## 📊 Recommended Learning Path

### Path 1: Complete Foundational Track (All Labs)
Lab 0 → Lab 1 → Lab 2 → Lab 3 → Lab 4 → Lab 5 → Lab 6 → Lab 7

**Best for**: Students wanting comprehensive understanding

### Path 2: Accelerated Track (Skip Theory)
Lab 0 → Lab 3 → Lab 4 → Lab 5 → Lab 6 → Lab 7

**Best for**: Those with ML background wanting practical skills

### Path 3: Problem-Focused Track (The Exact Match Problem)
Lab 0 → Lab 2 → Lab 5 → Lab 6

**Best for**: Solving specific business problems with RAG

---

## 🔧 Creating Your Own Labs

Want to adapt labs for your domain?

**Template**:
1. Define learning objectives (what students will learn)
2. Provide starter code with TODOs
3. Include realistic dataset
4. Add evaluation rubric
5. Include expected outputs for checking work

---

## 📦 Data Sources Reference

### Open-Source Datasets Used

| Lab | Dataset | Size | Source |
|-----|---------|------|--------|
| Lab 4 | MongoDB Restaurants | 25K documents | MongoDB Atlas |
| Lab 4 | MongoDB Movies | 23K documents | MongoDB Atlas |
| Lab 5 | Generated Exact-Match | 1K documents | Custom |
| Lab 6 | Hybrid Search Evaluation | 5K documents | Custom + Real |

**Downloading Datasets**:
All datasets are either generated or can be downloaded from MongoDB Atlas with a free account.

---

## 🎓 Grading Rubric (for Academic Use)

Each lab should be evaluated on:

1. **Correctness** (50%): Does the solution work?
2. **Understanding** (25%): Can student explain the concepts?
3. **Analysis** (15%): Did student analyze results and draw conclusions?
4. **Code Quality** (10%): Clean, well-documented, efficient?

---

## ✅ Prerequisites Checklist

Before starting labs:

- [ ] Python 3.9+ installed
- [ ] Comfortable with libraries: pandas, NumPy, scikit-learn
- [ ] Basic understanding of machine learning concepts
- [ ] Read through [Prerequisites section](../00-prerequisites/index.md)
- [ ] Jupyter notebooks setup and working

---

## 🚀 Getting Started

1. **Setup Environment**: Start with [Lab 0: Environment Setup](notebooks/lab_0_environment.ipynb)
2. **Choose Your Path**: Pick a learning path above
3. **Follow Sequentially**: Labs build on previous concepts
4. **Complete Exercises**: Each lab has TODOs and checkpoints
5. **Verify Results**: Compare against expected outputs

---

## 📝 Lab Structure You'll See

Each lab notebook contains:

```
1. Imports and Setup
2. Learning Objectives  ← What you'll learn
3. Concept Review       ← Theory reminder
4. Exercise 1, 2, 3     ← Hands-on TODOs
5. Checkpoint           ← Verify understanding
6. Challenge (Optional) ← Go deeper
7. Summary              ← Key takeaways
```

---

## 💡 Tips for Success

- **Don't Skip the Math**: Lab 1 builds intuition for everything after
- **Run the Code**: Don't just read; execute and experiment
- **Modify Examples**: Change parameters and see what happens
- **Try Challenges**: Optional exercises but highly rewarding
- **Take Notes**: Jot down key insights
- **Re-run Labs**: Concepts stick better on second run

---

**Ready to begin?** Start with [Lab 0: Environment Setup](notebooks/lab_0_environment.ipynb)

---

--8<-- "_abbreviations.md"
