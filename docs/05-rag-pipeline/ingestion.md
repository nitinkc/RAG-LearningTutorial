# Ingestion: Preparing Documents for RAG

The quality of your RAG system depends heavily on how well you prepare documents during ingestion.

## The Ingestion Pipeline

```
Raw Documents
    ↓
[Parsing] → Extract text, metadata, structure
    ↓
[Cleaning] → Remove noise, normalize
    ↓
[Chunking] → Split into retrievable pieces
    ↓
[Embedding] → Convert to vectors
    ↓
[Indexing] → Add to vector database + BM25
    ↓
Retrieval-Ready System
```

## Step 1: Parsing

Extract text and structure from various formats:

```python
from pathlib import Path
import PyPDF2
import json

def parse_document(file_path):
    """Parse different document types."""
    
    ext = Path(file_path).suffix.lower()
    
    if ext == '.pdf':
        return parse_pdf(file_path)
    elif ext == '.txt':
        return parse_text(file_path)
    elif ext == '.json':
        return parse_json(file_path)
    elif ext == '.csv':
        return parse_csv(file_path)
    else:
        raise ValueError(f"Unsupported format: {ext}")

def parse_pdf(file_path):
    """Extract text from PDF."""
    reader = PyPDF2.PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def parse_json(file_path):
    """Load structured JSON (e.g., orders)."""
    with open(file_path) as f:
        data = json.load(f)
    return data
```

## Step 2: Cleaning

Remove noise and normalize:

```python
import re

def clean_text(text):
    """Clean extracted text."""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters (keep alphanumeric and basic punctuation)
    text = re.sub(r'[^\w\s.,:;!?\-]', '', text)
    
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    return text.strip()

# Test
dirty = "This  is\n\n   messy!!!  www.spam.com"
clean = clean_text(dirty)
print(clean)  # "This is messy www.spam.com"
```

## Step 3: Chunking (Critical for Exact Match)

How you chunk determines retrieval quality. (See [Chunking Strategies](../04-exact-match/chunking-strategies.md) for detailed discussion.)

```python
def chunk_by_size(text, chunk_size=512, overlap=50):
    """Simple fixed-size chunking."""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    
    return chunks

def chunk_structured_data(document):
    """For structured data (orders, products)."""
    chunks = []
    
    # Key-value pairs
    for key, value in document.items():
        if key in ['id', 'order_id', 'sku', 'product_id']:
            # Put IDs prominently
            chunks.append(f"{key.upper()}: {value}")
        else:
            chunks.append(f"{key}: {value}")
    
    # Combined summary
    summary = " | ".join([f"{k}:{v}" for k, v in document.items()])
    chunks.append(summary)
    
    return chunks
```

## Step 4: Embedding

Convert chunks to vectors:

```python
from sentence_transformers import SentenceTransformer
import numpy as np
from tqdm import tqdm

def create_embeddings(chunks, model_name='all-MiniLM-L6-v2', batch_size=32):
    """Create embeddings for all chunks."""
    
    model = SentenceTransformer(model_name)
    embeddings = model.encode(
        chunks,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_tensor=False
    )
    
    return embeddings

chunks = ["chunk1", "chunk2", ...]
embeddings = create_embeddings(chunks)
print(embeddings.shape)  # (n_chunks, 384)
```

## Step 5: Indexing

Add to vector database and BM25:

```python
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from rank_bm25 import BM25Okapi
import re

def index_documents(documents, vector_db_url="http://localhost:6333"):
    """Index documents in vector DB and BM25."""
    
    # Initialize clients
    vector_client = QdrantClient(url=vector_db_url)
    
    # Create collection
    vector_client.create_collection(
        collection_name="documents",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    
    # Prepare embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    texts = [doc['text'] for doc in documents]
    embeddings = model.encode(texts)
    
    # Prepare BM25
    corpus = [text.lower().split() for text in texts]
    bm25 = BM25Okapi(corpus)
    
    #Upsert to vector DB
    points = []
    for i, (doc, emb) in enumerate(zip(documents, embeddings)):
        # Extract structured metadata
        order_id = re.search(r'Order #(\d+)', doc['text'])
        
        point = PointStruct(
            id=i,
            vector=emb,
            payload={
                'text': doc['text'],
                'source': doc.get('source', 'unknown'),
                'order_id': order_id.group(1) if order_id else None,
                'date': doc.get('date'),
            }
        )
        points.append(point)
    
    vector_client.upsert(
        collection_name="documents",
        points=points
    )
    
    # Save BM25 index
    import pickle
    with open('bm25_index.pkl', 'wb') as f:
        pickle.dump(bm25, f)
    
    return vector_client, bm25
```

## Complete Ingestion Pipeline

```python
class IngestionPipeline:
    def __init__(self, vector_db_url, model_name='all-MiniLM-L6-v2'):
        self.vector_db_url = vector_db_url
        self.encoder = SentenceTransformer(model_name)
    
    def ingest(self, documents):
        """Complete ingestion pipeline."""
        
        # 1. Parse
        parsed = [self.parse(doc) for doc in documents]
        
        # 2. Clean
        cleaned = [self.clean(text) for text in parsed]
        
        # 3. Chunk
        chunks = []
        for text in cleaned:
            chunks.extend(self.chunk(text))
        
        # 4. Embed
        embeddings = self.encoder.encode(chunks)
        
        # 5. Index
        self.index(chunks, embeddings)
        
        return len(chunks)
    
    def parse(self, doc_path):
        # Implement parsing
        pass
    
    def clean(self, text):
        # Implement cleaning
        pass
    
    def chunk(self, text):
        # Implement chunking (use structured for your case!)
        pass
    
    def index(self, chunks, embeddings):
        # Implement indexing to vector DB + BM25
        pass

# Usage
pipeline = IngestionPipeline("http://localhost:6333")
n_chunks = pipeline.ingest(["document1.pdf", "document2.json", ...])
print(f"Ingested {n_chunks} chunks")
```

## Best Practices

1. **Preserve Structure**: For orders/products, use structured chunking
2. **Keep IDs Prominent**: Order ID = first token in chunk
3. **Test Chunk Quality**: Verify chunks make sense independently
4. **Monitor Metadata**: Track extraction accuracy (especially IDs)
5. **Handle Failures**: Log and skip unparseable documents gracefully

## Next Step

→ [Retrieval & Augmentation](retrieval-augmentation.md) - Query processing
