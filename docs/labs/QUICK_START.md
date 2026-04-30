# RAG Labs - Quick Start Card

Print this! Keep it handy! 📋

---

## 🚀 START HERE (3 steps, 5 minutes)

### Step 1: Install Dependencies
```bash
cd docs/labs
pip install -r requirements-labs.txt
```

### Step 2: Launch Jupyter
```bash
jupyter notebook
```

### Step 3: Open Lab 0
- Browser opens at `http://localhost:8888`
- Navigate to: `notebooks/lab_0_environment.ipynb`
- Click first cell, press **Shift + Enter**

---

## 📍 Navigation Map

```
RAG Learning Tutorial (root)
└── docs/labs/
    ├── README_LABS.md          ← Overview
    ├── CURRICULUM_GUIDE.md     ← Study strategies
    ├── SETUP.md                ← Installation help
    │
    ├── notebooks/              ← Jupyter files here!
    │   ├── lab_0_environment.ipynb      START
    │   ├── lab_1_vector_math.ipynb      ← Vector math
    │   ├── lab_2_embeddings.ipynb       ← Embeddings
    │   ├── lab_3_chroma_basics.ipynb    ← Vector DB
    │   ├── lab_4_mongodb_ingestion.ipynb ← Real data
    │   ├── lab_5_exact_match_problem.ipynb ← The problem
    │   ├── lab_6_hybrid_search.ipynb    ← Solution
    │   └── lab_7_complete_rag.ipynb     ← Full system
    │
    └── data/
        ├── restaurants_sample.json  (10 records)
        └── exact_match_sample.json (10 records)
```

---

## ⏱️ Time Breakdown

| Lab | Duration | Difficulty |
|-----|----------|-----------|
| 0 | 30 min | ⭐ |
| 1 | 1.5 hr | ⭐⭐ |
| 2 | 1.5 hr | ⭐⭐ |
| 3 | 2 hr | ⭐⭐ |
| 4 | 2.5 hr | ⭐⭐⭐ |
| 5 | 2 hr | ⭐⭐⭐ |
| 6 | 2.5 hr | ⭐⭐⭐ |
| 7 | 3 hr | ⭐⭐⭐⭐ |
| **Total** | **15 hr** | - |

**Spread over**: 2-3 weeks (1 lab per session recommended)

---

## 🧠 What Each Lab Teaches

| Lab | Teaches | You'll Know |
|-----|---------|-----------|
| 0 | Setup | Environment ready |
| 1 | Vector math | Cosine similarity |
| 2 | Embeddings | SentenceTransformer |
| 3 | Vector DB | Chroma, HNSW |
| 4 | Ingestion | Real data pipelines |
| 5 | Problem | Why semantics fail |
| 6 | Solution | Hybrid search |
| 7 | Integration | Full RAG system |

---

## 🎯 Choose Your Path

**Beginner? Do ALL labs in order**
```
0 → 1 → 2 → 3 → 4 → 5 → 6 → 7
```

**ML exp? Skip 1-2**
```
0 → [read 1-2 summary] → 3 → 4 → 5 → 6 → 7
```

**Specific problem? Skip 3-4**
```
0 → 2 → 4 → 5 → 6
```

---

## 💡 Pro Tips

### Running a Cell
```
1. Click the cell
2. Press Shift + Enter
3. Wait for output
4. Read and understand
5. Modify and experiment!
```

### When Stuck
```
1. Reread the concept section
2. Modify code slightly
3. Check error message
4. Add print() statements
5. Try simpler test case
```

### Learning Best
```
✅ Code along (don't just read)
✅ Modify every example
✅ Try challenges (optional)
✅ Take notes on paper
✅ Explain to a friend
```

---

## 🔧 Troubleshooting Quick Fixes

**Import error?**
```bash
# Make sure venv is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

**Jupyter won't start?**
```bash
pip install jupyter --upgrade
jupyter notebook
```

**Cell runs forever?**
```
Press: Ctrl + C (stops execution)
```

**Too slow?**
```
CPU is fine. Patience! Each lab gets faster.
```

---

## 📊 What You'll Build

```
After Lab 0  → Working environment ✓
After Lab 1  → Understand vectors ✓
After Lab 2  → See embeddings work ✓
After Lab 3  → Queryable database ✓
After Lab 4  → Ingested real data ✓
After Lab 5  → Understand the problem ✓
After Lab 6  → Solution that works ✓
After Lab 7  → Complete RAG system ✓
```

---

## ✨ Key Concepts by Lab

| Lab | Concept | Formula / Code |
|-----|---------|---|
| 1 | Cosine Similarity | `1 - cosine_distance(v1, v2)` |
| 2 | Embedding | `model.encode("text")` |
| 3 | Vector Search | `collection.query(embedding)` |
| 4 | Chunking | Split document into 512-token pieces |
| 5 | Problem | Numbers look similar in embeddings |
| 6 | Fusion | Combine dense + BM25 rankings |
| 7 | Pipeline | Query → Embed → Search → Rank → Generate |

---

## 📚 Quick Command Reference

```python
# Embeddings (Lab 2)
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
embedding = model.encode("text here")

# Vector DB (Lab 3)
import chromadb
client = chromadb.PersistentClient(path="./data")
collection = client.get_or_create_collection("docs")

# BM25 Search (Lab 6)
from rank_bm25 import BM25Okapi
bm25 = BM25Okapi(tokenized_corpus)
scores = bm25.get_scores(tokenized_query)
```

---

## ✅ Success Criteria

Each lab is **successful** if:
- ✅ Code runs without errors
- ✅ You understand the output
- ✅ You can explain the concept
- ✅ You tried a modification
- ✅ You know when to use it

---

## 🎓 After Labs Complete

You can now:
- ✅ Build semantic search systems
- ✅ Solve exact-match problems  
- ✅ Create RAG pipelines
- ✅ Evaluate search quality
- ✅ Optimize for production

---

## 📞 Support Resources

| Need | Resource |
|------|----------|
| Installation | SETUP.md |
| Learning strategy | CURRICULUM_GUIDE.md |
| Lab overview | README_LABS.md |
| Theory background | docs/ (main site) |
| Data sources | data/README.md |

---

## 🚀 Next Action

Open Terminal:
```bash
cd docs/labs
pip install -r requirements-labs.txt
jupyter notebook
```

Then navigate to `notebooks/lab_0_environment.ipynb`

---

**You've got this! 💪**

Questions? Check CURRICULUM_GUIDE.md → Getting Help section

Errors? Check SETUP.md → Troubleshooting section

---

*RAG Learning Tutorial - Practical Labs*  
*College-Level Academic Program*  
*Learn by Doing ✓*
