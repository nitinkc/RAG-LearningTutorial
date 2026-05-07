# Evaluation: Measuring RAG Quality

How do you know if your RAG system is working well? This section covers metrics and evaluation strategies.

## Key Metrics

### Retrieval Metrics

**Mean Reciprocal Rank (MRR)**: Position of first relevant document

```
Query: "Order #1766"
Results: [Order #1767, ✓Order #1766, ...]
MRR = 1/2 = 0.5 (first relevant at position 2)
```

**Recall@K**: What percentage of relevant docs are in top-K?

```
Relevant: {#1766, #1767 info, tracking}
Retrieved top-3: {#1766, tracking, other}
Recall@3 = 2/3 = 0.67 (found 2 out of 3)
```

**NDCG**: How well are results ranked?

```python
from sklearn.metrics import ndcg_score

y_true = [1, 1, 0, 0]  # Relevant scores
y_score = [0.9, 0.8, 0.7, 0.6]  # Predicted scores

ndcg = ndcg_score([y_true], [y_score])
```

### Generation Metrics

**Faithfulness**: Is the answer grounded in context?

```
Question: "What's my order status?"
Context: "Order #1766 shipped..."
Answer: "Your order shipped"
Faithfulness: HIGH (answer matches context)

vs

Answer: "Your order is delivered"
Faithfulness: LOW (contradicts context)
```

**Relevance**: Does answer address question?

```
Question: "When will my order arrive?"
Answer: "Your order shipped yesterday"
Relevance: HIGH

vs

Answer: "We have many shipping carriers"
Relevance: LOW (doesn't answer WHEN)
```

## RAGAS Framework

Modern RAG evaluation:

```python
from ragas import evaluate
from ragas.metrics import faithfulness, relevance, context_recall

# Prepare data
eval_data = {
    'question': ["What about Order #1766?"],
    'answer': ["Order #1766 is shipped"],
    'context': [["Order #1766 shipped via FedEx"]],
    'ground_truth': ["Order #1766 shipped"]
}

# Evaluate
score = evaluate(eval_data, metrics=[faithfulness, relevance, context_recall])
print(score)  # Prints overall scores
```

## Simple Evaluation Script

```python
def evaluate_rag_system(test_queries):
    """Simple evaluation of RAG system."""
    
    results = {
        'mrr': [],
        'retrieval_accuracy': [],
        'answer_quality': []
    }
    
    for query, expected_answer in test_queries:
        # Retrieve
        retrieved = retrieve(query)
        
        # Generator
        answer = generate(query, retrieved)
        
        # Metrics
        mrr = calculate_mrr(retrieved, expected_answer)
        accuracy = answer_matches(answer, expected_answer)
        quality = human_eval_score(answer)  # Manual scoring
        
        results['mrr'].append(mrr)
        results['retrieval_accuracy'].append(accuracy)
        results['answer_quality'].append(quality)
    
    # Summarize
    return {
        'avg_mrr': np.mean(results['mrr']),
        'retrieval_acc': np.mean(results['retrieval_accuracy']),
        'quality': np.mean(results['answer_quality'])
    }
```

## Test Cases for Your System

For Order #1766 exact match problem:

```python
exact_match_tests = [
    {
        'query': 'What about Order #1766?',
        'expected_source': 'should_contain_1766',
        'should_not_contain': ['#1767', '#1765'],
        'metric': 'exact_match_only'
    },
    {
        'query': 'Tell me about order 1766',  # Written differently
        'expected_source': 'should_contain_1766',
        'metric': 'fuzzy_match'
    },
    {
        'query': 'What is my order status?',  # Semantic query
        'expected_source': 'should_contain_recent_order',
        'metric': 'semantic_despite_id'
    }
]

# Run tests
for test in exact_match_tests:
    results = retrieve(test['query'])
    sources = [r.text for r in results]
    
    # Check assertions
    assert any(test['expected_source'] in s for s in sources), \
        f"Failed: {test['query']}"
    
    assert not any(bad in s for bad in test.get('should_not_contain', []) for s in sources), \
        f"Found unwanted source in {test['query']}"
    
    print(f"✓ Passed: {test['query']}")
```

## Monitoring in Production

Track system health over time:

```python
import logging
from datetime import datetime

class RAGMonitor:
    def __init__(self, log_file="rag_metrics.log"):
        self.logger = logging.getLogger("rag_system")
        self.handler = logging.FileHandler(log_file)
        self.logger.addHandler(self.handler)
    
    def log_query(self, query, retrieved, answer, metrics):
        """Log a query execution."""
        
        self.logger.info({
            'timestamp': datetime.now(),
            'query': query,
            'n_retrieved': len(retrieved),
            'latency_ms': metrics['latency'],
            'answer_length': len(answer),
            'confidence': metrics['confidence'],
            'error': metrics.get('error')
        })
    
    def report(self, time_window_hours=24):
        """Generate report for recent queries."""
        
        # Filter logs by time window
        # Calculate averages
        # Return report
        pass
```

## Benchmarking Against Baselines

Compare your RAG system:

```python
def benchmark_comparison():
    """Compare different strategies."""
    
    methods = {
        'semantic_only': SemanticRetriever(),
        'keyword_only': BM25Retriever(),
        'hybrid': HybridRetriever(),
        'hybrid_with_filter': HybridRetrieverWithFilter(),
        'hybrid_with_rerank': HybridRetrieverWithReranking()
    }
    
    results = {}
    
    for method_name, retriever in methods.items():
        metrics = evaluate_rag_system(test_queries, retriever)
        results[method_name] = metrics
        
        print(f"{method_name}:")
        print(f"  MRR: {metrics['mrr']:.3f}")
        print(f"  Recall@10: {metrics['recall']:.3f}")
        print(f"  Latency: {metrics['latency']:.0f}ms")
    
    # Show improvement
    baseline = results['semantic_only']['mrr']
    for method, metrics in results.items():
        improvement = (metrics['mrr'] - baseline) / baseline * 100
        print(f"{method} improvement: {improvement:+.1f}%")
```

## Debugging Failed Predictions

```python
def debug_retrieval_failure(query, expected_doc_id):
    """Understanding why a query failed."""
    
    # Retrieve all stages
    dense_results = dense_search(query)
    sparse_results = sparse_search(query)
    hybrid_results = combine(dense_results, sparse_results)
    
    print(f"Query: {query}")
    print(f"\nDense search results:")
    for r in dense_results[:3]:
        is_target = "✓" if r.id == expected_doc_id else " "
        print(f"  {is_target} [{r.id}] score={r.score:.3f}: {r.text[:50]}...")
    
    print(f"\nSparse search results:")
    for r in sparse_results[:3]:
        is_target = "✓" if r.id == expected_doc_id else " "
        print(f"  {is_target} [{r.id}] score={r.score:.3f}: {r.text[:50]}...")
    
    print(f"\nHybrid combined:")
    for r in hybrid_results[:5]:
        is_target = "✓" if r.id == expected_doc_id else " "
        print(f"  {is_target} [{r.id}] score={r.score:.3f}")
    
    # Identify failure point
    if expected_doc_id not in [r.id for r in dense_results[:100]]:
        print("\n→ FAILED at dense search stage")
    elif expected_doc_id not in [r.id for r in sparse_results[:100]]:
        print("\n→ FAILED at sparse search stage")
    elif expected_doc_id not in [r.id for r in hybrid_results[:10]]:
        print("\n→ FAILED at combination/ranking stage")
    else:
        print("\n→ Retrieved but ranked too low")
```

## Summary Table

| Metric | What It Measures | Good Value | How to Improve |
|--------|-----------------|-----------|---|
| MRR | Rank of 1st relevant | > 0.7 | Better ranking/re-ranking |
| Recall@10 | % relevant found | > 0.8 | Increase top-K retrieval |
| Faithfulness | Answer matches context | > 0.8 | Better prompt engineering |
| Relevance | Answer addresses question | > 0.8 | Better retrieval |
| Latency | Time to answer | < 200ms | Optimize retrieval |

## Final Recommendation

**Always measure before and after optimizations:**

```python
# Before change
baseline = evaluate_rag_system(test_queries)
print(f"Baseline MRR: {baseline['mrr']:.3f}")

# Make change (e.g., add re-ranking)
implement_change()

# After change
improved = evaluate_rag_system(test_queries)
print(f"Improved MRR: {improved['mrr']:.3f}")
print(f"Improvement: {(improved['mrr'] - baseline['mrr'])*100:+.1f}%")

# Check trade-offs
print(f"Latency change: {improved['latency'] - baseline['latency']:+.0f}ms")
```

---

Congrats! You now understand RAG from first principles. 🎉

--8<-- "_abbreviations.md"
