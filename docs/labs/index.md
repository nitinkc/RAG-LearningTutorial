# RAG Practical Labs: Hands-On Learning

Welcome to the labs track. These notebooks are structured as college-level exercises that move from foundations to advanced RAG system design.

## At a Glance

- **Format**: Jupyter notebooks with guided exercises and checkpoints
- **Time per lab**: ~1 to 3 hours
- **Difficulty path**: Foundations -> Intermediate -> Advanced
- **Skills covered**: Python, vector math, embeddings, vector databases, retrieval, evaluation

## Learning Roadmap

| Lab  | Topic                                   | Level                 | Time   | Primary Outcome                 |
|:-----|:----------------------------------------|:----------------------|:-------|:--------------------------------|
| 0    | Environment Setup                       | Foundations           | 30 min | Working local environment       |
| 1    | Vector Math and Distance Metrics        | Foundations           | 1.5 hr | Core similarity math intuition  |
| 2    | Text Embeddings and Semantic Similarity | Foundations           | 1.5 hr | Embedding analysis workflow     |
| 3    | Vector Databases with Chroma            | Intermediate          | 2 hr   | Persisted vector search system  |
| 4    | Real Data Ingestion (MongoDB -> Chroma) | Intermediate          | 2.5 hr | End-to-end ingestion pipeline   |
| 5    | Exact vs Semantic Match Problem         | Intermediate          | 2 hr   | Failure analysis and diagnosis  |
| 6    | Hybrid Search Implementation            | Intermediate-Advanced | 2.5 hr | Dense+sparse retrieval pipeline |
| 7    | Complete RAG Pipeline                   | Advanced              | 3 hr   | Full system with evaluation     |

## Lab Details

### Lab 0: Environment Setup and Fundamentals

- **Notebook**: [lab_0_environment.ipynb](notebooks/lab_0_environment.ipynb)
- **You will learn**:
  - Create and use a Python virtual environment
  - Install required packages and validate imports
  - Verify CPU/GPU runtime basics
  - Run first embedding examples
- **Deliverable**: Working environment and successful setup checks

### Lab 1: Vector Math and Distance Metrics

- **Notebook**: [lab_1_vector_math.ipynb](notebooks/lab_1_vector_math.ipynb)
- **You will learn**:
  - Implement dot product, norms, normalization
  - Compare cosine, Euclidean, and Manhattan metrics
  - Build geometric intuition in 2D/3D
- **Deliverable**: Working vector ops and metric comparison visuals

### Lab 2: Text Embeddings and Semantic Similarity

- **Notebook**: [lab_2_embeddings.ipynb](notebooks/lab_2_embeddings.ipynb)
- **You will learn**:
  - Generate embeddings with SentenceTransformer
  - Inspect embedding dimensions and distribution
  - Analyze semantic similarity and nearest neighbors
  - Visualize clusters with dimensionality reduction
- **Deliverable**: Embedding corpus analysis and similarity outputs

### Lab 3: Vector Databases with Chroma

- **Notebook**: [lab_3_chroma_basics.ipynb](notebooks/lab_3_chroma_basics.ipynb)
- **You will learn**:
  - Create and populate a Chroma index
  - Store vectors with metadata
  - Query, update, delete, and persist data
  - Understand ANN/HNSW behavior at a practical level
- **Deliverable**: Working vector database with metadata-aware search

### Lab 4: Real Data Ingestion (MongoDB to Chroma)

- **Notebook**: [lab_4_mongodb_ingestion.ipynb](notebooks/lab_4_mongodb_ingestion.ipynb)
- **You will learn**:
  - Load open datasets and preprocess records
  - Apply chunking strategies
  - Preserve metadata through ingestion
  - Batch embed and insert at scale
- **Deliverable**: Ingested dataset with chunked vectors and metadata

### Lab 5: Exact vs Semantic Match (Core RAG Failure Mode)

- **Notebook**: [lab_5_exact_match_problem.ipynb](notebooks/lab_5_exact_match_problem.ipynb)
- **You will learn**:
  - Reproduce exact-match failure cases (for example, close IDs)
  - Visualize why semantic similarity can return wrong exact records
  - Identify when dense-only retrieval is insufficient
- **Deliverable**: Failure analysis and decision criteria for hybrid search

### Lab 6: Hybrid Search Implementation

- **Notebook**: [lab_6_hybrid_search.ipynb](notebooks/lab_6_hybrid_search.ipynb)
- **You will learn**:
  - Implement sparse retrieval (BM25/TF-IDF)
  - Combine dense and sparse ranks with RRF
  - Compare retrieval quality across methods
  - Evaluate with ranking metrics (for example, MRR/NDCG)
- **Deliverable**: Hybrid retrieval pipeline with comparative evaluation

### Lab 7: Complete RAG Pipeline

- **Notebook**: [lab_7_complete_rag.ipynb](notebooks/lab_7_complete_rag.ipynb)
- **You will learn**:
  - Connect ingestion, retrieval, and generation
  - Implement multi-stage retrieval and ranking
  - Evaluate relevance, faithfulness, and latency
  - Discuss production concerns (monitoring, cost, performance)
- **Deliverable**: End-to-end RAG prototype with evaluation results

## Data Sources

| Lab  | Dataset                   | Approx Size   | Source                      |
|:-----|:--------------------------|:--------------|:----------------------------|
| 4    | MongoDB Restaurants       | 25K documents | MongoDB Atlas sample data   |
| 4    | MongoDB Movies            | 23K documents | MongoDB Atlas sample data   |
| 5    | Exact-match synthetic set | 1K documents  | Generated in lab            |
| 6    | Hybrid evaluation set     | 5K documents  | Mixed generated + real data |

All datasets are generated in-lab or available through free-tier public/sample sources.

## Prerequisites Checklist

Before starting labs:

- [ ] Python 3.9+ installed
- [ ] Basic comfort with pandas, NumPy, and scikit-learn
- [ ] Basic machine learning familiarity
- [ ] Read [Prerequisites section](../00-prerequisites/index.md)
- [ ] Jupyter notebooks open and running locally

## How to Use These Labs

1. Start with [Lab 0](notebooks/lab_0_environment.ipynb) and verify setup.
2. Progress in order (each lab builds on earlier concepts).
3. Complete TODOs and checkpoint sections.
4. Compare outputs and write short observations.
5. Re-run selected labs after finishing Lab 7 to reinforce intuition.

## Academic Evaluation Rubric (Optional)

- **Correctness (50%)**: Solution works and satisfies the prompt
- **Understanding (25%)**: Concepts are explained clearly
- **Analysis (15%)**: Results are interpreted with reasoning
- **Code Quality (10%)**: Code is readable, structured, and reproducible

## Tips for Success

- Do not skip Lab 1 math intuition; it improves all later labs.
- Execute every cell and modify parameters to see behavior changes.
- Keep brief notes on errors, fixes, and metric changes.
- Prefer small, reproducible experiments before scaling up.

Ready to begin: [Lab 0 - Environment Setup](notebooks/lab_0_environment.ipynb)

--8<-- "_abbreviations.md"
