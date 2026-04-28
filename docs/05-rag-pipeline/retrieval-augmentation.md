# Retrieval & Augmentation: Building Context

After ingestion, the retrieval phase finds relevant documents and uses them to augment the LLM prompt.

## Retrieval Strategy (Recap)

Use the **complete hybrid approach** you've learned:

```python
def retrieve(query, vector_db, bm25, top_k=10):
    """Hybrid retrieval with filtering."""
    
    # 1. Extract constraints
    constraints = extract_constraints(query)
    
    # 2. Dense search
    dense_results = vector_db.search(
        query_embedding,
        limit=100
    )
    
    # 3. Sparse search
    sparse_results = bm25.search(query, top_k=100)
    
    # 4. Combine (hybrid)
    hybrid = combine_results(dense_results, sparse_results)
    
    # 5. Filter by constraints
    filtered = [r for r in hybrid if passes_filter(r, constraints)]
    
    # 6. Return top-K
    return filtered[:top_k]
```

## Context Assembly

Convert retrieved documents into prompt context:

```python
def assemble_context(retrieved_results, max_context_length=2000):
    """Build context string for LLM."""
    
    context_parts = []
    total_length = 0
    
    for i, result in enumerate(retrieved_results):
        # Format: "Source N: [text]"
        formatted = f"Source {i+1} (confidence: {result.score:.2f}):\n{result.text}"
        
        if total_length + len(formatted) > max_context_length:
            break
        
        context_parts.append(formatted)
        total_length += len(formatted)
    
    return "\n\n".join(context_parts)

# Usage
context = assemble_context(top_results)
# Output:
# Source 1 (confidence: 0.95):
# Order #1766 confirmed...
#
# Source 2 (confidence: 0.92):
# Order #1766 tracking...
```

## Prompt Engineering

Build effective prompts that use retrieved context:

```python
class RAGPromptBuilder:
    def build_prompt(self, query, context, system_role="customer service"):
        """Build prompt with context for LLM."""
        
        if system_role == "customer service":
            return f"""
You are a helpful customer service assistant.
Use the provided documentation to answer customer questions accurately and courteously.
If the information is not in the documentation, say you don't have that information.

Documentation:
{context}

Customer Question: {query}

Answer:
"""
        
        elif system_role == "order specialist":
            return f"""
You are an order tracking specialist.
Use the order information provided to give accurate status updates.
Always cite the source when providing information.

Order Information:
{context}

Customer Question: {query}

Answer (with source citation):
"""
    
    def build_chat_prompt(self, conversation_history, context):
        """Build prompt for multi-turn conversation."""
        
        messages = [
            {
                "role": "system",
                "content": f"""You are a helpful assistant.
Use this context to inform your answers:

{context}"""
            }
        ]
        
        for user_msg, assistant_msg in conversation_history[:-1]:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": assistant_msg})
        
        messages.append({"role": "user", "content": conversation_history[-1]})
        
        return messages
```

## Managing Context Window

LLMs have limited context (4K-8K tokens typical):

```python
def optimize_context(query, retrieved_results, max_tokens=2000):
    """Use most relevant context within token limit."""
    
    # Estimate tokens (rough: 1 token ≈ 4 chars)
    query_tokens = len(query) / 4
    overhead_tokens = 200  # Prompt template, instructions
    available = max_tokens - query_tokens - overhead_tokens
    
    # Prioritize by score
    sorted_results = sorted(retrieved_results, key=lambda x: x.score, reverse=True)
    
    context_parts = []
    used_tokens = 0
    
    for result in sorted_results:
        result_tokens = len(result.text) / 4
        
        if used_tokens + result_tokens > available:
            break
        
        context_parts.append(result.text)
        used_tokens += result_tokens
    
    return "\n\n".join(context_parts)
```

## Retrieval with Follow-up Questions

For complex queries, retrieve multiple times:

<details>
<summary>Click to expand code example</summary>

```python
def iterative_retrieval(initial_query, vector_db, max_iterations=3):
    """Refine retrieval through multiple steps."""
    
    all_results = []
    current_query = initial_query
    seen_ids = set()
    
    for iteration in range(max_iterations):
        # Retrieve for current query
        results = retrieve(current_query, vector_db)
        
        # Deduplicate
        new_results = [r for r in results if r.id not in seen_ids]
        all_results.extend(new_results)
        seen_ids.update(r.id for r in new_results)
        
        # Generate follow-up question
        # (In real system, LLM would generate this)
        follow_up = generate_follow_up(current_query, results)
        
        if not follow_up:
            break
        
        current_query = follow_up
    
    return all_results
```

</details>

## Quality Metrics

Track retrieval quality during augmentation:

```python
def evaluate_retrieval(query, retrieved_results, ground_truth_ids):
    """Measure retrieval quality."""
    
    retrieved_ids = {r.id for r in retrieved_results}
    
    # Recall: how many relevant docs did we find?
    recall = len(retrieved_ids & ground_truth_ids) / len(ground_truth_ids)
    
    # Precision: how many retrieved docs were relevant?
    precision = len(retrieved_ids & ground_truth_ids) / len(retrieved_ids)
    
    # Mean Reciprocal Rank: how early was the first relevant?
    mrr = 0
    for i, result in enumerate(retrieved_results):
        if result.id in ground_truth_ids:
            mrr = 1 / (i + 1)
            break
    
    return {
        'recall': recall,
        'precision': precision,
        'mrr': mrr,
        'f1': 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    }
```

## Next Step

→ [Generation](generation.md) - LLM interaction and answer generation
