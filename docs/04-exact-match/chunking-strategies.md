# Chunking Strategies: Preserving Token Identity

How you split documents into chunks dramatically affects retrieval quality, especially for exact matches.

## The Chunking Problem

What you embed and index matters more than you might think.

### Bad Chunking: Loss of Context

```
Documents:
  "Customer John Doe placed Order #1766 on 2024-01-15 
   with items {laptop, mouse, keyboard} totaling $3,500.
   Shipping address: 123 Main St. Order #1766 will ship
   within 2 business days..."

Naive Chunking (by size, 200 chars):
  Chunk 1: "Customer John Doe placed Order #1766 on 2024-01-15 
            with items {laptop, mouse, keyboard} totaling..."
  
  Chunk 2: "...totaling $3,500. Shipping address: 123 Main St. 
            Order #1766 will ship within 2 business days..."

Problem: Order ID appears in the middle/end of chunks,
         loses prominence when compared sidestep with other orders
```

### Good Chunking: Preserving Identity

```
Structured Chunking (for Order #1766):
  
  Chunk 1: "ORDER_ID: #1766"
  Chunk 2: "Order #1766 Customer: John Doe"
  Chunk 3: "Order #1766 Date: 2024-01-15"
  Chunk 4: "Order #1766 Items: {laptop, mouse, keyboard}"
  Chunk 5: "Order #1766 Total: $3,500"
  Chunk 6: "Order #1766 Shipping: 123 Main St"
  Chunk 7: "Order #1766 Delivery: within 2 business days"

Benefit: Order ID appears at the BEGINNING of every chunk,
         making it prominent in embeddings and BM25 scoring
```

## Chunking Strategies

### Strategy 1: Naive Fixed-Size

```
Document: "A long text..."
Split every 256 tokens (overlap 64):

Chunk 1: tokens[0:256]
Chunk 2: tokens[192:448]  (192 = 256 - 64 overlap)
Chunk 3: tokens[384:640]
...
```

**Pros**: Simple  
**Cons**: Might split sentences, loses structure, bad for exact matches

```python
def naive_chunking(text, chunk_size=256, overlap=64):
    words = text.split()
    chunks = []
    
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(' '.join(words[start:end]))
        start = end - overlap
    
    return chunks
```

### Strategy 2: Semantic (Sentence-Based)

```
Document: "Customer placed order. Status: confirmed. 
           Shipping tomorrow..."

Split by sentences:

Chunk 1: "Customer placed order."
Chunk 2: "Status: confirmed."
Chunk 3: "Shipping tomorrow..."
```

**Pros**: Respects sentence boundaries, natural  
**Cons**: Loses context between sentences

```python
import nltk
from nltk.tokenize import sent_tokenize

def semantic_chunking(text):
    return sent_tokenize(text)
```

### Strategy 3: Recursive (Sentences → Smaller Units)

```
Document structure:
  ├─ Section 1
  │  └─ Paragraph
  │      └─ Sentence 1
  │      └─ Sentence 2

Split at largest boundaries first, then smaller:

Chunks = [
    [Sentence 1, Sentence 2],  # Try keeping sentences together
    [Sentence 1],              # If too big, split
    [Sentence 2]
]
```

**Pros**: Respects document structure  
**Cons**: More complex

### Strategy 4: Structured (FOR RAG—Best for IDs/Exact Matches)

**For documents with structured data (orders, products, accounts):**

```python
def structured_chunking(document):
    """
    Extract structured fields and create separate chunks.
    Perfect for orders, products, profiles, etc.
    """
    chunks = []
    
    # Field-level chunks (Order ID most prominent)
    if 'order_id' in document:
        chunks.append(f"ORDER_ID: {document['order_id']}")
    
    if 'customer_name' in document:
        chunks.append(f"Order #{document['order_id']} Customer: {document['customer_name']}")
    
    if 'created_date' in document:
        chunks.append(f"Order #{document['order_id']} Date: {document['created_date']}")
    
    if 'items' in document:
        items_str = ', '.join(document['items'])
        chunks.append(f"Order #{document['order_id']} Items: {items_str}")
    
    if 'total' in document:
        chunks.append(f"Order #{document['order_id']} Total: {document['total']}")
    
    # Full summary (for context)
    summary = f"Order #{document['order_id']}: {document.get('status', 'pending')} - {len(document.get('items', []))} items"
    chunks.append(summary)
    
    return chunks

# Example
order = {
    'order_id': '1766',
    'customer_name': 'John Doe',
    'created_date': '2024-01-15',
    'items': ['laptop', 'mouse'],
    'total': '$3,500',
    'status': 'shipped'
}

chunks = structured_chunking(order)
# Chunks:
# ["ORDER_ID: 1766",
#  "Order #1766 Customer: John Doe",
#  "Order #1766 Date: 2024-01-15",
#  ...,
#  "Order #1766: shipped - 2 items"]
```

**Pros**: 
- ✅ IDs always prominent
- ✅ Perfect for structured data
- ✅ Works well with BM25 (exact match)
- ✅ Works well with metadata filtering

**Cons**: 
- ❌ Requires knowing document structure
- ❌ Less suitable for unstructured text

### Strategy 5: Hybrid (Structured + Semantic)

Combine structured and unstructured:

```python
def hybrid_chunking(document):
    """
    For documents with both structured and unstructured parts.
    """
    chunks = []
    
    # 1. Structured chunks (ID-focused)
    if 'order_id' in document:
        chunks.append(f"ORDER_ID: {document['order_id']}")
        chunks.append(f"Order #{document['order_id']} Status: {document.get('status', 'unknown')}")
    
    # 2. Semantic chunks (description/notes)
    if 'description' in document:
        description_chunks = sent_tokenize(document['description'])
        for i, chunk in enumerate(description_chunks):
            # Prepend ID for prominence
            full_chunk = f"Order #{document['order_id']}: {chunk}"
            chunks.append(full_chunk)
    
    # 3. Include context for key dates/amounts
    if 'created_date' in document:
        chunks.append(f"Order #{document['order_id']} Placed: {document['created_date']}")
    
    return chunks
```

## Chunking Strategy: Task-Based Decision

```
Is your data...

Structured?  (orders, products, accounts)
├─ Use structured chunking
├─ Put ID/key at beginning of EACH chunk
└─ Create separate chunks per field

Unstructured? (articles, PDFs, news)
├─ Use semantic (sentence-based)
├─ But prepend important IDs/keywords to chunks
└─ Use recursive if very long

Mixed? (structured + narrative)
└─ Use hybrid approach
```

## Example: Orders vs Articles

### Orders (Structured)

```python
order_doc = {
    'order_id': '1766',
    'customer': 'john@example.com',
    'date': '2024-01-15',
    'items': [
        {'sku': 'LAPTOP-001', 'name': 'Dell Laptop', 'qty': 1, 'price': 1200},
        {'sku': 'MOUSE-002', 'name': 'Wireless Mouse', 'qty': 2, 'price': 50},
    ],
    'total': 1300,
    'status': 'shipped'
}

# Structured chunking - best approach
chunks = [
    "ORDER_ID: 1766",
    "Order #1766 Customer: john@example.com",
    "Order #1766 Date: 2024-01-15",
    "Order #1766 Status: shipped",
    "Order #1766 Item: LAPTOP-001 Dell Laptop (Qty: 1, Price: $1200)",
    "Order #1766 Item: MOUSE-002 Wireless Mouse (Qty: 2, Price: $50 each)",
    "Order #1766 Total: $1300"
]
```

### Articles (Unstructured)

```python
article = {
    'title': 'How to Use Embeddings',
    'url': 'https://example.com/article-123',
    'body': "Embeddings are... They work by... Applications include..."
}

# Semantic chunking (but prepend context)
chunks = [
    "Article 'How to Use Embeddings': Embeddings are vector representations of text...",
    "Article 'How to Use Embeddings': They work by training neural networks on large corpora...",
    "Article 'How to Use Embeddings': Applications include search, recommendation systems, and more..."
]
```

## Impact on Retrieval Quality

### Without Good Chunking

```
Query: "Order #1766"

Dense Search Results:
- Order #1766 ... in middle of 500-token chunk ≈ 0.87 similarity
- Order #1767 ... in middle of 500-token chunk ≈ 0.86 similarity
- ❌ Can't distinguish by embedding alone

BM25 Results (if not chunked well):
- Order #1766 ... buried in text, low TF ≈ 3.2 score
- Order #1767 ... nearby, similar TF ≈ 3.1 score
- ❌ Similar scores
```

### With Good Structured Chunking

```
Query: "Order #1766"

Dense Search Results:
- "ORDER_ID: 1766" ≈ 0.95 similarity (very specific)
- "Order #1766 Status: shipped" ≈ 0.93 similarity
- ❌ Still might mix with #1767

BM25 Results:
- "ORDER_ID: 1766" ≈ 8.5 score (exact match at START)
- "Order #1766 Customer: ..." ≈ 8.3 score
- ✅ #1767 chunks don't match "1766" at all!

Hybrid Combined:
- "ORDER_ID: 1766" →  0.95 + 8.5 = 9.45 ✅
- "Order #1766 ..." → 0.93 + 8.3 = 9.23 ✅  
- #1767 chunks → ~0.85 + 0 = 0.85 (lost!)
```

## Best Practices

1. **Put important identifiers FIRST in chunks**
   ```
   ✅ "Order #1766: Customer John Doe..."
   ❌ "Customer John Doe placed Order #1766 on..."
   ```

2. **Create separate chunks for structured fields**
   ```
   ✅ Chunk 1: "ORDER_ID: 1766"
      Chunk 2: "Order #1766 Status: shipped"
   ❌ Chunk 1: "Order 1766 is shipped and customer is John Doe..."
   ```

3. **Repeat context in each chunk**
   ```
   ✅ "Order #1766: [description]"
      "Order #1766: [tracking]"
      "Order #1766: [address]"
   ❌ "[description]"
      "[tracking]"  
      "[address]"
   ```

4. **Keep chunks reasonably-sized**
   ```
   256-512 tokens for dense retrieval
   Allow overlap (50-100 tokens) to preserve context
   ```

5. **Test with your actual queries**
   ```python
   # Benchmark different chunking strategies
   for strategy in [strategy1, strategy2, strategy3]:
       chunks = strategy(documents)
       index_chunks(chunks)
       mrr = evaluate_with_queries(test_queries)
       print(f"Strategy {name}: MRR = {mrr}")
   ```

## Code Example: Comparing Chunking Strategies

```python
from sentence_transformers import SentenceTransformer

doc = """
Order #1766 placed by john@example.com on 2024-01-15.
Items: Dell Laptop ($1200), Wireless Mouse x2 ($50 each).
Total: $1300. Status: shipped. Tracking: FedEx.
Arrives by Jan 20, 2024.
"""

# Strategy A: Naive
naive_chunks = naive_chunking(doc, chunk_size=100)

# Strategy B: Structured
structured_chunks = structured_chunking({
    'order_id': '1766',
    'customer': 'john@example.com',
    'date': '2024-01-15',
    'items': ['Dell Laptop', 'Wireless Mouse'],
    'total': '$1300',
    'status': 'shipped'
})

# Compare embeddings
encoder = SentenceTransformer('all-MiniLM-L6-v2')

query = "Order #1766"
query_emb = encoder.encode(query)

print("Naive chunking:")
for i, chunk in enumerate(naive_chunks):
    sim = cosine_similarity(query_emb, encoder.encode(chunk))
    print(f"  Chunk {i}: {sim:.3f} - '{chunk[:50]}...'")

print("\nStructured chunking:")
for i, chunk in enumerate(structured_chunks):
    sim = cosine_similarity(query_emb, encoder.encode(chunk))
    print(f"  Chunk {i}: {sim:.3f} - '{chunk}'")

# Structured chunking will show higher similarity for ID-focused chunks!
```

## Summary

| Strategy | Best For | Considers IDs? | Support Exact Match? |
|----------|----------|---|---|
| Naive | Quick prototypes | ❌ No | ❌ Poor |
| Semantic | Unstructured text | ❌ No | ⚠ Medium |
| Recursive | Large documents | ❌ No | ⚠ Medium |
| **Structured** | **Orders, products, profiles** | ✅ Yes | ✅ Great |
| Hybrid | Mixed documents | ✅ Yes | ✅ Great |

## Recommendation

**For RAG systems with exact identifiers (Order #1766, SKU-001, etc.):**
- Use **structured chunking**
- Put IDs at the BEGINNING of every chunk
- Create separate chunks per field

This maximally helps:
- Dense retrieval (ID prominent in embedding)
- Sparse retrieval (BM25 scores ID matches highest)
- Metadata filtering (IDs easy to extract)

## Next Steps

→ [RAG Pipeline](../05-rag-pipeline/index.md) — Putting everything together
