# Generation: LLM Integration

The final step: using the LLM with retrieved context to generate answers.

## Basic Generation

```python
from openai import OpenAI

def generate_answer(query, context, model="gpt-3.5-turbo"):
    """Generate answer using LLM."""
    
    client = OpenAI(api_key="your-key")
    
    prompt = f"""
Use the following context to answer the question.
If you don't know, say so.

Context:
{context}

Question: {query}

Answer:
"""
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content
```

## With Citation

Track which sources were used:

```python
def generate_with_citations(query, retrieved_results, model="gpt-3.5-turbo"):
    """Generate answer with source citations."""
    
    # Build context with source markers
    context = "\n\n".join([
        f"[Source {i+1}]: {result.text}"
        for i, result in enumerate(retrieved_results)
    ])
    
    prompt = f"""
Answer the question using the provided sources.
Cite sources by referring to [Source N] when relevant.
If not in sources, say you don't know.

{context}

Question: {query}

Answer:
"""
    
    response = generate(prompt, model)
    
    # Extract source references
    citations = extract_citations(response, len(retrieved_results))
    
    return {
        'answer': response,
        'sources': [retrieved_results[i] for i in citations],
        'confidence': calculate_confidence(citations, len(retrieved_results))
    }
```

## Streaming Response

For better UX, stream LLM output:

```python
def generate_streaming(query, context):
    """Stream answer as it's generated."""
    
    client = OpenAI()
    
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"{context}\n\n{query}"}
        ],
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
```

## Handling Long Contexts

When context is very long, use summarization:

```python
def summarize_context(long_context, max_tokens=500):
    """Summarize long context to fit in model."""
    
    client = OpenAI()
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"Summarize this in {max_tokens} tokens:\n{long_context}"
            }
        ],
        max_tokens=max_tokens
    )
    
    return response.choices[0].message.content
```

## Advanced: Chain-of-Thought

Improve reasoning by asking LLM to think step-by-step:

```python
def generate_with_reasoning(query, context):
    """Use chain-of-thought prompting."""
    
    prompt = f"""
Context:
{context}

Question: {query}

Think step by step:
1. What information from the context is relevant?
2. How does it address the question?
3. What is the final answer?

Answer:
"""
    
    return generate(prompt)
```

## Multi-Turn Conversation

Maintain conversation history:

```python
class RAGConversation:
    def __init__(self, vector_db):
        self.vector_db = vector_db
        self.history = []
    
    def ask(self, user_message):
        """Process user message and maintain context."""
        
        # Retrieve based on latest message
        context = self.retrieve(user_message)
        
        # Build messages with history
        messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        
        # Add conversation history (limit to recent 5 exchanges)
        for user_msg, assistant_msg in self.history[-5:]:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": assistant_msg})
        
        # Add current message with context
        messages.append({
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {user_message}"
        })
        
        # Generate response
        response = generate(messages)
        
        # Store in history
        self.history.append((user_message, response))
        
        return response
    
    def retrieve(self, message):
        # Hybrid retrieval logic
        pass
```

## Confidence Scoring

Estimate answer confidence:

```python
def score_confidence(answer, context, retrieved_scores):
    """Estimate how confident the answer is."""
    
    factors = {
        'source_quality': sum(retrieved_scores) / len(retrieved_scores),  # Avg retrieval score
        'answer_length': min(len(answer.split()) / 100, 1.0),  # Longer = more detail
        'source_count': min(len(retrieved_scores) / 3, 1.0),   # More sources = better
    }
    
    # Weighted average
    weights = {'source_quality': 0.5, 'answer_length': 0.2, 'source_count': 0.3}
    confidence = sum(factors[k] * weights[k] for k in factors)
    
    return min(confidence, 1.0)  # Cap at 1.0
```

## Error Handling

Gracefully handle failures:

```python
def generate_safe(query, context, model="gpt-3.5-turbo"):
    """Generate with fallback."""
    
    try:
        # Try primary model
        return generate(query, context, model)
    
    except TokenLimitError:
        # Reduce context
        summarized = summarize_context(context, max_tokens=500)
        return generate(query, summarized, model)
    
    except APIError as e:
        # Fall back to simpler extraction
        return extract_answer_from_context(query, context)
    
    except Exception as e:
        # Last resort: return context itself
        return f"Unable to process. Here's the relevant information:\n{context}"
```

## Next Step

→ [Evaluation](evaluation.md) - Measuring system quality
