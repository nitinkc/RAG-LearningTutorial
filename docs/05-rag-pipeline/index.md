# RAG Pipeline: End-to-End Architecture

Now that you understand all the components (embeddings, retrieval, filtering), let's build a complete RAG system.

## RAG Architecture Overview

```
┌────────────────────────────────────────────────────┐
│                    DATA INGESTION                  │
├────────────────────────────────────────────────────┤
│  Raw Documents → Chunking → Embedding → Indexing  │
└─────────────────────────────────┬──────────────────┘
                                  │
                    Vector Database (HNSW)
                    BM25 Index
                    Metadata Store
                                  │
┌─────────────────────────────────┴──────────────────┐
│                  RETRIEVAL PHASE                   │
├────────────────────────────────────────────────────┤
│  Query → Extract Constraints → [Dense + Sparse]   │
│           ↓          ↓          ↓                  │
│  Hybrid Combination → Filtering → Re-ranking       │
└─────────────────────────────────┬──────────────────┘
                                  │
                            Top-K Results
                                  │
┌─────────────────────────────────┴──────────────────┐
│               AUGMENTATION PHASE                   │
├────────────────────────────────────────────────────┤
│  Prompt Template → Context Assembly → LLM Input   │
└─────────────────────────────────┬──────────────────┘
                                  │
┌─────────────────────────────────┴──────────────────┐
│               GENERATION PHASE                     │
├────────────────────────────────────────────────────┤
│  LLM (Prompt + Context) → Answer + Citations      │
└────────────────────────────────────────────────────┘
```

## Topics Covered

- [Ingestion](ingestion.md) — Chunking, embedding, indexing documents
- [Retrieval & Augmentation](retrieval-augmentation.md) — Query → retrieve → augment prompt
- [Generation](generation.md) — LLM interaction and prompt engineering
- [Evaluation](evaluation.md) — Metrics to measure RAG system quality

## The Pipeline Flow

### 1. Ingestion (Build Time)

```python
# Load documents
documents = load_documents('orders_database')

# Chunk intelligently
chunks = [chunk_document(doc) for doc in documents]

# Create embeddings
embeddings = [encode(chunk) for chunk in chunks]

# Index
vector_db.index(embeddings, chunks)
bm25_index.index(chunks)

# Store metadata
metadata_store.store({
    'chunk_id': chunk_id,
    'order_id': extract_order_id(chunk),
    'date': extract_date(chunk),
    ...
})
```

### 2. Retrieval (Query Time)

```python
# User asks
query = "What about Order #1766?"

# Extract constraints
order_id = extract_order_id(query)

# Dense search
dense_results = vector_db.search(encode(query), k=100)

# Sparse search
sparse_results = bm25_index.search(query, k=100)

# Combine
hybrid = combine(dense_results, sparse_results)

# Filter
if order_id:
    filtered = [r for r in hybrid if r.order_id == order_id]
else:
    filtered = hybrid

# Re-rank
ranked = reranker.rank(filtered, query)

top_k = ranked[:10]
```

### 3. Augmentation (Prompt Building)

```python
# Build context from retrieved results
context = "\n".join([f"- {result}" for result in top_k])

# Create prompt
prompt_template = """
Use the following context to answer the question.
If you don't know the answer, say so.

Context:
{context}

Question: {question}

Answer:
"""

prompt = prompt_template.format(context=context, question=query)
```

### 4. Generation (LLM Call)

```python
# Call LLM
response = llm.generate(prompt, max_tokens=500)

# Extract answer with citations
answer = response.text
citations = extract_citations(top_k, response)

return {
    'answer': answer,
    'sources': citations,
    'confidence': calculate_confidence(response, context)
}
```

## End-to-End Example

```python
class RAGSystem:
    def __init__(self, vector_db_path, llm_model):
        self.vector_db = load_vector_db(vector_db_path)
        self.bm25 = load_bm25_index(vector_db_path)
        self.llm = llm_model
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    
    def query(self, query_text, top_k=10):
        """End-to-end RAG."""
        
        # === RETRIEVAL ===
        
        # 1. Extract constraints
        order_id = extract_order_id(query_text)
        
        # 2. Dense retrieval
        query_emb = self.encoder.encode(query_text)
        dense_results = self.vector_db.search(query_emb, k=100)
        
        # 3. Sparse retrieval
        tokens = query_text.lower().split()
        sparse_scores = self.bm25.get_scores(tokens)
        sparse_results = get_top_k(sparse_scores, k=100)
        
        # 4. Hybrid combination
        hybrid = self.combine_results(dense_results, sparse_results)
        
        # 5. Metadata filtering
        if order_id:
            filtered = [r for r in hybrid if r.metadata.get('order_id') == order_id]
        else:
            filtered = hybrid
        
        # 6. Re-ranking
        pairs = [[query_text, r.text] for r in filtered]
        rerank_scores = self.reranker.predict(pairs)
        ranked = sorted(zip(filtered, rerank_scores), key=lambda x: x[1], reverse=True)
        
        top_results = [r[0] for r in ranked[:top_k]]
        
        # === AUGMENTATION ===
        context = "\n\n".join([
            f"Source {i+1}:\n{result.text}"
            for i, result in enumerate(top_results)
        ])
        
        # === GENERATION ===
        prompt = f"""
        You are a helpful customer service assistant.
        Use the provided order information to answer the customer's question.
        If information is not available, say so.
        
        Order Information:
        {context}
        
        Customer Question: {query_text}
        
        Answer:
        """
        
        response = self.llm.generate(prompt, temperature=0.7, max_tokens=500)
        
        return {
            'answer': response.text,
            'sources': [{'id': r.id, 'text': r.text} for r in top_results],
            'retrieval_time': time.time()
        }
    
    def combine_results(self, dense, sparse, w_dense=0.5):
        """Combine dense and sparse results."""
        # Implementation from previous section
        pass
```

## Performance Considerations

### Latency Budget

```
Query → Response Time: ~100-200ms target

├─ Embedding: ~20ms
├─ Dense search in vector DB: ~15ms
├─ Sparse search in BM25: ~10ms
├─ Filtering: ~5ms
├─ Re-ranking (optional): ~50ms
├─ LLM generation: ~100-500ms (dominant!)
└─ Total: ~150-700ms
```

For faster response:
- Skip re-ranking (saves ~50ms)
- Use smaller LLM (faster but lower quality)
- Use prompt caching (OpenAI, Anthropic)

### Memory Requirements

```
1 million documents, 384-dim embeddings:

Vector DB (HNSW): ~2 GB
BM25 Index: ~500 MB
Metadata Store: ~100 MB
LLM in memory: ~5-20 GB (depends on model)
────────────────
Total: ~8-23 GB
```

### Throughput

```
Single query: ~100-200ms (including LLM)
Batch queries: ~50-100 queries/min (LLM bottleneck)
Concurrent users: ~10-50 (depends on infrastructure)
```

## Quality Improvement Strategies

| Strategy | Latency Impact | Quality Impact | Cost |
|----------|---|---|---|
| Hybrid search | +5ms | +5% | None (built-in) |
| Re-ranking | +50ms | +7% | Small |
| Larger LLM | +100ms | +5% | Medium |
| Prompt engineering | ~0ms | +10% | None (effort) |
| Fine-tuning embeddings | ~0ms | +15% | High |
| Multi-stage retrieval | +100ms | +8% | Small |

## Deployment Considerations

### Single Server
```
- Best for: <100K documents, <10 QPS
- Cost: $10-50/month
- Easy to manage
```

### Distributed System
```
- Best for: >1M documents, >100 QPS
- Cost: $100-1000/month
- Requires orchestration (Kubernetes)
```

### Serverless
```
- Best for: Variable load, small team
- Cost: Pay per query ($0.01-0.50 per query)
- Limited debugging, cold starts
```

## Monitoring & Observability

```python
# Track key metrics
metrics = {
    'retrieval_latency': 45,  # ms
    'generation_latency': 250,  # ms
    'mrr': 0.82,  # Mean Reciprocal Rank
    'answer_relevance': 0.89,  # Using RAGAS
    'user_satisfaction': 4.2,  # Out of 5
    'cost_per_query': 0.02,   # USD
}

# Log for monitoring
logger.info(f"Query processed: {metrics}")
```

### Key Metrics to Track

1. **Retrieval Quality**
   - MRR (Mean Reciprocal Rank)
   - NDCG (Normalized Discounted Cumulative Gain)
   - Top-K recall

2. **Generation Quality**
   - Faithfulness (is answer grounded in context?)
   - Relevance (does answer address question?)
   - Fluency (is answer well-written?)

3. **System Performance**
   - Latency (time to answer)
   - Throughput (queries per second)
   - Error rates

4. **Cost**
   - Cost per query
   - Cost per user
   - ROI of improvements

## Next Steps

→ [Ingestion](ingestion.md) — Document preparation

→ [Retrieval & Augmentation](retrieval-augmentation.md) — Query processing

→ [Generation](generation.md) — LLM interaction

→ [Evaluation](evaluation.md) — Measuring quality

--8<-- "_abbreviations.md"
