# References and Further Reading

## Papers and Foundational Work

### Embeddings & Similarity Search

- **Vector Search** (2023) - Review of modern vector search techniques
- **Dense Passage Retrieval** (Karpukhin et al., 2020) - DPR for open-domain QA
- **Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks** (Reimers & Gupta, 2019) - Foundation of modern sentence embeddings

### Retrieval

- **BM25 Algorithm** (Robertson et al., 1994) - Seminal work on probabilistic ranking
- **Hybrid Search: Combining Dense and Sparse Retrieval** (Various, 2023) - Modern hybrid approaches
- **Learning to Rank** (Liu, 2009) - Foundations for re-ranking

### RAG

- **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** (Lewis et al., 2020) - Original RAG paper
- **Improving Language Models by Retrieving from Trillions of Tokens** (Borgeaud et al., 2022) - Gato / RETRO
- **Evaluating Retrieval-Augmented Generation Systems** (Various, 2023) - Evaluation frameworks

## Libraries and Tools

### Vector Databases

- **Qdrant** - https://qdrant.tech/ - Modern vector database
- **Pinecone** - https://www.pinecone.io/ - Managed vector search
- **Weaviate** - https://weaviate.io/ - Vector database with GraphQL
- **Chroma** - https://www.trychroma.com/ - Lightweight embedding database
- **FAISS** - https://github.com/facebookresearch/faiss - Facebook's vector search library
- **Milvus** - https://milvus.io/ - Open-source similarity search engine

### Embedding Models

- **Sentence Transformers** - https://www.sbert.net/ - Pre-trained sentence embeddings
- **Hugging Face** - https://huggingface.co/models - Model hub
- **OpenAI Embeddings** - https://platform.openai.com/docs/guides/embeddings - Production embeddings API

### BM25 & Sparse Search

- **Elasticsearch** - https://www.elastic.co/ - Production search engine
- **rank-bm25** - Python library for BM25 scoring
- **Apache Lucene** - Java-based search library

### LLM Frameworks

- **LangChain** - https://www.langchain.com/ - Framework for building RAG applications
- **LlamaIndex** - https://www.llamaindex.ai/ - Data framework for LLMs
- **Haystack** - https://haystack.deepset.ai/ - NLP framework for building search systems

### Evaluation

- **RAGAS** - Framework for evaluating RAG systems
- **TREC Evaluation** - Standard IR evaluation metrics
- **Weights & Biases** - https://wandb.ai/ - Experiment tracking

## Getting Started Resources

### Tutorials

- **Sentence Transformers Documentation** - https://sbert.net/ tutorials
- **LangChain RAG Tutorial** - https://python.langchain.com/docs/use_cases/question_answering/
- **Qdrant Getting Started** - https://qdrant.tech/documentation/

### Blog Posts and Articles

- "Vector Search in Production" - Engineering blogs from Pinecone, Qdrant, Weaviate
- "Hybrid Search Techniques" - Modern retrieval methods
- "RAG System Design" - Architecture and best practices

## Quick Reference

### Math Concepts

| Concept | Formula | Use |
|---------|---------|-----|
| Cosine Similarity | $\frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\|\|\vec{v}\|}$ | Embedding similarity |
| Euclidean Distance | $\sqrt{\sum (u_i - v_i)^2}$ | Distance-based search |
| TF-IDF | TF × IDF | Keyword scoring |
| BM25 | IDF × TF/(k1 + TF × (1 - b + b*L)) | Ranking function |
| RRF Score | 1/k + Σ 1/(k + rank) | Rank fusion |

### Libraries Comparison

| Library | Purpose | Ease | Performance |
|---------|---------|------|-------------|
| FAISS | Vector search | Easy | Fast |
| Chroma | Embedding DB | Very Easy | Medium |
| Qdrant | Vector DB | Easy | Very Fast |
| Pinecone | Managed VectorDB | Easy | Depends on plan |
| Weaviate | Vector DB | Medium | Fast |
| Elasticsearch | Full search | Hard | Very Fast |

### Python Packages

```bash
# Core packages
pip install sentence-transformers  # Embeddings
pip install qdrant-client         # Vector DB
pip install rank-bm25             # BM25 search
pip install langchain             # RAG framework
pip install openai                # LLM API

# Evaluation
pip install ragas                 # RAG evaluation
pip install datasets              # Benchmark datasets

# Visualization
pip install jupyter               # Interactive notebooks
pip install umap-learn            # Dimensionality reduction
```

## Key Takeaways

1. **Embeddings** capture semantic meaning but fail on exact matches
2. **BM25/Sparse search** finds exact keywords but misses meaning
3. **Hybrid search** combines both for best results
4. **Metadata filtering** provides hard constraints (Order ID exact match)
5. **Chunking strategy** determines how prominent information becomes
6. **Re-ranking** improves results when latency allows
7. **Evaluation** is critical: track MRR, relevance, faithfulness

## Quick Tips

### For Development

```python
# Fast prototyping
from sentence_transformers import SentenceTransformer
from chroma-core import Chroma

embeddings = SentenceTransformer('all-MiniLM-L6-v2')
vectordb = Chroma.from_documents(docs, embeddings)
```

### For Production

```python
# Use distributed vector DB
from qdrant_client import QdrantClient

client = QdrantClient(url="http://vector-db:6333")
results = client.search(collection_name="documents", ...)

# Use hybrid with LangChain
from langchain.retrievers import BM25Retriever, MMRRetriever
# Combine multiple retrievers
```

### For Debugging

```python
# Check embedding quality
from umap import UMAP
embeddings_2d = UMAP(n_components=2).fit_transform(all_embeddings)
# Visualize clusters

# Check retrieval
for query in test_queries:
    results = retrieve(query)
    print(f"Query: {query}")
    for r in results[:3]:
        print(f"  - {r.text}: {r.score:.3f}")
```

## Staying Updated

- **Papers**: ArXiv cs.CL, cs.IR
- **Blogs**: Hugging Face blog, LangChain documentation, vector DB blogs
- **Communities**: r/MachineLearning, Papers with Code forums
- **Conferences**: SIGIR (information retrieval), NeurIPS, ACL (NLP)

## Related Topics to Explore

1. **Fine-tuning Embeddings** - Improve quality for specific domains
2. **Multi-hop Retrieval** - Chain multiple retrieval steps
3. **Knowledge Graphs** - Structured information as retrieval backbone
4. **Prompt Engineering** - Optimize LLM prompts for better answers
5. **Agents** - Give LLMs ability to iteratively refine retrieval
6. **Multi-modal RAG** - Combine text, images, and structured data

--8<-- "_abbreviations.md"

