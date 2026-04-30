# Lab Data Sources & Setup Guide

## Open-Source MongoDB Datasets

All MongoDB sample datasets are publicly available and free to use for educational purposes.

### MongoDB Atlas Sample Datasets

MongoDB provides free sample datasets that you can use directly. No credit card needed for local development.

#### 1. Restaurants Dataset (25K documents)
- **Size**: ~24,000 documents
- **Fields**: name, address, borough, cuisine, grades, phone, website
- **Perfect for**: Lab 4 (ingestion) and Lab 6 (hybrid search)
- **Use Case**: Restaurant search and recommendation

**Quick Start**:
```python
# Option 1: Download JSON directly (see script below)
# Option 2: Use MongoDB Atlas (free tier)
# Option 3: Load from provided restaurants.json in /data folder
```

#### 2. Movies Dataset (23K documents)
- **Size**: ~23,000 documents
- **Fields**: title, plot, genres, runtime, imdb rating, cast, directors
- **Perfect for**: Lab 4 and semantic search on descriptions
- **Use Case**: Movie/media recommendation system

---

## Data Download Instructions

### For Local Development (Recommended)

**Option A**: Download Pre-sampled Data from This Project
```bash
cd docs/labs/data/
# Files will be provided (restaurants_sample.json, movies_sample.json)
```

**Option B**: Download from MongoDB via Python
```python
import json
import urllib.request

# Restaurants dataset
url = "https://raw.githubusercontent.com/mongodb/mongo-python-driver/master/bson/json_util.py"
# Or use MongoDB Atlas sample datasets directly

# Instructions in Lab 4
```

**Option C**: Use MongoDB Atlas (Free Account)
1. Create free MongoDB Atlas account: https://www.mongodb.com/cloud/atlas
2. Create free cluster (512MB storage)
3. Load sample dataset from Atlas UI
4. Connect via connection string in python

---

## How Laboratory Data is Used

### Lab 4: MongoDB Ingestion Pipeline
- **Dataset**: Restaurants (or Movies)
- **Process**:
  1. Load ~1000 documents
  2. Extract text fields (name, cuisine, reviews)
  3. Chunk documents (fixed-size or semantic)
  4. Generate embeddings
  5. Store in Chroma with metadata
  
**Expected Output**: Vector database with 1000-5000 chunks

### Lab 5: Exact Match Problem
- **Dataset**: Generated custom dataset with order IDs
- **Challenge**: Order #1766 vs #1767 issue
- **Solution**: Hybrid search

### Lab 6: Hybrid Search Evaluation
- **Dataset**: Restaurants reviews + structured metadata
- **Comparison**: Semantic vs Keyword vs Hybrid
- **Metric**: How many top-3 results are truly relevant

---

## Sample Data Included

This project includes smaller sample datasets (500 documents each) in:
- `docs/labs/data/restaurants_sample.json` (500 restaurants)
- `docs/labs/data/exact_match_sample.json` (100 order records)
- `docs/labs/data/hybrid_test_set.json` (200 documents with references)

These are perfect for testing locally without downloading large files.

---

## Data Schema Reference

### Restaurants JSON Structure
```json
{
  "_id": "ObjectId",
  "name": "Restaurant Name",
  "address": {
    "street": "123 Main St",
    "zipcode": "10001",
    "borough": "Manhattan",
    "coord": [-73.9, 40.7]
  },
  "cuisine": "Italian",
  "phone": "212-555-1234",
  "grades": [
    {
      "date": "2021-01-15",
      "grade": "A",
      "score": 13
    }
  ],
  "website": "http://example.com"
}
```

### Movies JSON Structure
```json
{
  "_id": "ObjectId",
  "title": "Movie Title",
  "plot": "Full plot description...",
  "genres": ["Action", "Drama"],
  "runtime": 120,
  "rated": "PG-13",
  "imdb": {
    "rating": 8.5,
    "votes": 250000
  },
  "cast": ["Actor 1", "Actor 2"],
  "directors": ["Director 1"],
  "year": 2021
}
```

---

## License & Attribution

- **MongoDB Sample Datasets**: Creative Commons License - see https://www.mongodb.com/docs/atlas/sample-data/
- **Custom Datasets**: Created for educational purposes

---

## Troubleshooting Data Issues

**Issue**: "File not found"
- **Solution**: Download sample data using Lab 4 instructions

**Issue**: "Encoding errors reading JSON"
- **Solution**: Specify UTF-8 encoding: `open(file, encoding='utf-8')`

**Issue**: "Out of memory with full dataset"
- **Solution**: Use provided sample datasets or limit documents: `json_data[:1000]`

---

## Next Steps

1. **Lab 4**: Will guide you through loading this data
2. **Create vector embeddings**: Convert text fields to vectors
3. **Store in database**: Chunk and embed at scale
4. **Evaluate results**: Measure quality of retrieval

See [Lab 4: MongoDB Ingestion](../notebooks/lab_4_mongodb_ingestion.ipynb) for detailed walkthrough.

---

--8<-- "_abbreviations.md"
