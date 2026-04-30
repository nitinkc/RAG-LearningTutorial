# 📚 RAG Learning Tutorial - Practical Labs

A comprehensive college-level academic program teaching **Retrieval-Augmented Generation** from first principles through hands-on coding labs.

---

## 🎯 What You'll Build

By working through 8 progressive labs, you'll build expertise in:

```
Vector Math → Embeddings → Vector Databases → Data Ingestion
    ↓              ↓              ↓                  ↓
 [Lab 1]      [Lab 2]        [Lab 3]           [Lab 4]
                    ↓
        Problem-solving: Exact Match Issue
                    ↓
    Semantic vs Keyword vs Hybrid Search
             [Labs 5-6]
                    ↓
            Complete RAG Pipeline
                  [Lab 7]
```

---

## 📊 Lab Overview

| # | Lab Name | Level | Time | Focus |
|---|----------|-------|------|-------|
| **0** | Environment Setup | ⭐ | 30 min | Configuration |
| **1** | Vector Math & Metrics | ⭐⭐ | 1.5 hrs | Math Foundations |
| **2** | Text Embeddings | ⭐⭐ | 1.5 hrs | BERT Models |
| **3** | Vector Databases | ⭐⭐ | 2 hrs | Chroma VectorDB |
| **4** | MongoDB Ingestion | ⭐⭐⭐ | 2.5 hrs | Real Data Pipelines |
| **5** | Exact vs Semantic | ⭐⭐⭐ | 2 hrs | Problem Analysis |
| **6** | Hybrid Search | ⭐⭐⭐ | 2.5 hrs | BM25 + Dense |
| **7** | Complete RAG | ⭐⭐⭐⭐ | 3 hrs | End-to-End System |

**Total Time**: 14-15 hours spread over 2-3 weeks

---

## 📁 Project Structure

```
docs/labs/
├── index.md                          # Labs overview
├── CURRICULUM_GUIDE.md              # This guide
├── SETUP.md                          # Installation instructions
├── requirements-labs.txt             # Python dependencies
│
├── notebooks/                        # Jupyter notebooks (executable)
│   ├── lab_0_environment.ipynb
│   ├── lab_1_vector_math.ipynb
│   ├── lab_2_embeddings.ipynb
│   ├── lab_3_chroma_basics.ipynb
│   ├── lab_4_mongodb_ingestion.ipynb
│   ├── lab_5_exact_match_problem.ipynb
│   ├── lab_6_hybrid_search.ipynb
│   └── lab_7_complete_rag.ipynb
│
├── data/                             # Sample datasets
│   ├── README.md                     # Data guide
│   ├── restaurants_sample.json       # 10 restaurant records (ingestion demo)
│   └── exact_match_sample.json       # 10 orders (exact match problem)
│
└── [source files will be created as you work]
```

---

## 🚀 Quick Start (5 Minutes)

### 1. Choose Your Path

**Path A: Complete Beginner** (Recommended)
- Time: 14-15 hours
- Does all labs sequentially
- Best for: Learning everything

**Path B: Experienced with ML**
- Time: 11-12 hours  
- Skips Labs 1-2 (assumes vector math knowledge)
- Best for: Focused on RAG specifics

**Path C: Solving a Specific Problem**
- Time: 9-10 hours
- Labs: 0 → 2 → 4 → 5 → 6
- Best for: Production issues

### 2. Set Up Environment

```bash
cd docs/labs
pip install -r requirements-labs.txt
jupyter notebook
```

See [SETUP.md](SETUP.md) for detailed instructions.

### 3. Start Learning

Open `notebooks/lab_0_environment.ipynb` and follow the cells.

---

## 📖 Detailed Lab Descriptions

### **Lab 0: Environment Setup** (Foundation)
- **Duration**: 30 minutes
- **You'll learn**: Installation, library verification, first embedding
- **Deliverable**: Working Jupyter environment
- **Key code**: Load SentenceTransformer, create first embedding, verify setup
- **Start here**: [lab_0_environment.ipynb](notebooks/lab_0_environment.ipynb)

### **Lab 1: Vector Math & Distance Metrics** (Foundation)
- **Duration**: 1.5 hours
- **You'll learn**: 
  - Implement dot product, magnitude, normalization from scratch
  - Compare Euclidean, Manhattan, Cosine distance
  - Visualize vectors in 2D/3D space
  - Understand why cosine similarity works for embeddings
- **Deliverable**: Working implementations + visualizations
- **Key insight**: Cosine similarity = angle between vectors, perfect for text
- **Start here**: [lab_1_vector_math.ipynb](notebooks/lab_1_vector_math.ipynb)

### **Lab 2: Text Embeddings & Semantic Similarity** (Foundation)
- **Duration**: 1.5 hours
- **You'll learn**:
  - Load pretrained SentenceTransformer models
  - Generate embeddings for diverse texts
  - Explore embedding properties (dimensions, range, distribution)
  - Visualize semantic clustering with t-SNE
- **Deliverable**: Embedding analysis + similarity matrices
- **Key insight**: Similar texts → similar vectors automatically
- **Start here**: [lab_2_embeddings.ipynb](notebooks/lab_2_embeddings.ipynb)

### **Lab 3: Vector Databases with Chroma** (Intermediate)
- **Duration**: 2 hours
- **You'll learn**:
  - Create and populate a Chroma vector database
  - Store embeddings with metadata
  - Perform similarity search
  - Understand HNSW indexing
  - Delete, update, and persist vectors
- **Deliverable**: Working vector database with 100+ documents
- **Key insight**: Vector databases optimize similarity search at scale
- **Start here**: [lab_3_chroma_basics.ipynb](notebooks/lab_3_chroma_basics.ipynb)

### **Lab 4: Real Data Ingestion - MongoDB** (Intermediate)
- **Duration**: 2.5 hours
- **You'll learn**:
  - Load MongoDB open-source dataset (restaurants or movies)
  - Implement chunking strategies
  - Handle metadata preservation
  - Batch embed at scale
  - Measure ingestion performance
- **Data included**: restaur ants_sample.json (10 records)
- **Deliverable**: Ingested database with 1000+ chunks
- **Key insight**: Data pipeline engineering is critical for RAG
- **Start here**: [lab_4_mongodb_ingestion.ipynb](notebooks/lab_4_mongodb_ingestion.ipynb)

### **Lab 5: The Exact Match Problem** (Intermediate)
- **Duration**: 2 hours
- **Problem statement**: 
  - User searches for "Order #1766"
  - System returns "Order #1767" (semantically similar!)
  - This is wrong for exact-match queries
- **You'll learn**:
  - Why embeddings can't distinguish similar numbers
  - Visualize the problem in 2D space
  - Identify real-world failure cases
  - Understand the limitation theoretically
- **Deliverable**: Analysis + visualization of problem
- **Key insight**: Semantic search ≠ keyword search
- **Start here**: [lab_5_exact_match_problem.ipynb](notebooks/lab_5_exact_match_problem.ipynb)

### **Lab 6: Hybrid Search Implementation** (Intermediate-Advanced)
- **Duration**: 2.5 hours
- **Solution**: Combine semantic (dense) + keyword (sparse) retrieval
- **You'll learn**:
  - Implement BM25 sparse ranking
  - Score documents with TF-IDF
  - Implement Reciprocal Rank Fusion (RRF)
  - Compare: semantic vs keyword vs hybrid
  - Evaluate with metrics (MRR, NDCG)
- **Deliverable**: Working hybrid search system
- **Performance**: 95%+ better than pure semantic for exact matches
- **Start here**: [lab_6_hybrid_search.ipynb](notebooks/lab_6_hybrid_search.ipynb)

### **Lab 7: Complete RAG Pipeline** (Advanced)
- **Duration**: 3 hours
- **Complexity**: Full end-to-end system
- **You'll learn**:
  - System architecture and data flow
  - Multi-stage retrieval pipeline
  - Evaluation frameworks
  - Performance optimization
  - Production considerations
  - Monitoring and debugging
- **Deliverable**: Production-ready RAG system
- **Advanced topics**: Reranking, LLM integration, caching
- **Start here**: [lab_7_complete_rag.ipynb](notebooks/lab_7_complete_rag.ipynb)

---

## 🔧 Technical Stack

### Dependencies
- **Python**: 3.9+
- **Embeddings**: sentence-transformers (BERT-based)
- **Vector DB**: Chroma (local, persistent)
- **Ranking**: rank-bm25 (TF-IDF variant)
- **Visualization**: matplotlib, scikit-learn
- **Notebooks**: Jupyter

### Installation
```bash
pip install -r requirements-labs.txt
```

See [SETUP.md](SETUP.md) for troubleshooting.

---

## 📚 Sample Datasets

### Included in repo:
- **restaurants_sample.json** (10 restaurants, diverse cuisines)
- **exact_match_sample.json** (10 orders with similar IDs)

### Available online:
- **MongoDB Restaurants** (25,000 documents) - via MongoDB Atlas
- **MongoDB Movies** (23,000 documents) - via MongoDB Atlas
- **Hugging Face Datasets** (various options)

See [data/README.md](data/README.md) for usage instructions.

---

## Learning Outcomes

After completing these labs, you'll be able to:

### Knowledge
✅ Explain how embeddings capture semantic meaning  
✅ Describe vector database architecture and indexing  
✅ Articulate the exact match problem and solution  
✅ Compare dense vs sparse vs hybrid retrieval  
✅ Design data ingestion pipelines  

### Skills
✅ Implement vector math from scratch  
✅ Work with sentence transformer models  
✅ Create and query vector databases  
✅ Build BM25 ranking systems  
✅ Combine multiple ranking signals  
✅ Evaluate search quality with metrics  

### Applications
✅ Build semantic search systems  
✅ Implement exact-match solutions  
✅ Create RAG pipelines  
✅ Debug failing retrieval systems  
✅ Optimize search performance  

---

## 🎓 Academic Rigor

These labs follow **college-level standards**:

- **Progressive complexity**: Each lab builds on previous
- **Theory + Practice**: Math concepts explained then implemented
- **Real data**: Use actual MongoDB and domain datasets
- **Evaluation**: Measure and compare approaches
- **Challenge exercises**: Optional go-deeper problems
- **Grading rubric**: Understand what "complete" means

Suitable for:
- Computer Science students (IR, NLP, ML tracks)
- Software Engineering courses (Large-scale systems)
- Data Science programs (Practical applications)
- Self-study (Independent learners)

---

## 📖 How to Use This Program

### For Self-Study
1. Read [CURRICULUM_GUIDE.md](CURRICULUM_GUIDE.md) first
2. Choose your learning path
3. Setup environment ([SETUP.md](SETUP.md))
4. Work through labs in sequence
5. Complete exercises and challenges
6. Reflect on learnings

### For Classroom/Bootcamp
1. Assign labs in order (one per week)
2. Use grading rubric from [CURRICULUM_GUIDE.md](CURRICULUM_GUIDE.md)
3. Have students present findings
4. Group projects: Build RAG for chosen domain
5. Capstone: Optimize and evaluate system

### For Reference/Documentation
- Check specific lab for implementation details
- Use data/README.md for dataset info  
- See SETUP.md for environment issues
- Review CURRICULUM_GUIDE.md for learning strategies

---

## 🆘 Getting Help

### Troubleshooting
1. Check [SETUP.md](SETUP.md) - Common installation issues
2. Review lab-specific troubleshooting at bottom of notebook
3. Check error messages carefully
4. Simplify to minimal test case
5. Google the exact error message

### Understanding Concepts
1. Reread the relevant markdown section
2. Look up concept in [Theory Documentation](../)
3. Watch related explanations
4. Implement from scratch
5. Teach someone else

### Code Issues
1. Add print statements to debug
2. Check variable types with `type()`
3. Start with smaller dataset
4. Run cell-by-cell to isolate issue
5. Compare with expected output

---

## ✨ Key Insights from Each Lab

| Lab | Key Insight |
|-----|-------------|
| 0 | Tools matter - good setup prevents frustration |
| 1 | Cosine similarity = angle between vectors |
| 2 | Transformers learn to embed similar texts nearby |
| 3 | HNSW makes search practical at scale |
| 4 | Data engineering is 80% of RAG work |
| 5 | Embeddings capture "meaning" but not "exact value" |
| 6 | Combining signals > single signal |
| 7 | Systems thinking: parts must work together |

---

## 🚀 After Completing Labs

### What's Next?
1. **Build a project**: Apply to your domain data
2. **Explore tools**: LangChain, LlamaIndex, Qdrant
3. **Read papers**: RAG, embeddings, dense retrieval
4. **Production**: Deploy learned concepts to real system
5. **Teach others**: Explain RAG to colleagues

### Recommended Reading
- Original RAG paper (Lewis et al., 2020)
- BERT paper (Devlin et al., 2019)
- Dense passage retrieval (Karpukhin et al., 2020)
- Hybrid retrieval best practices

---

## 📊 Statistics

- **Total lines of code**: 2000+
- **Notebooks**: 8 complete, executable notebooks
- **Exercises**: 20+ hands-on exercises
- **Challenge problems**: 10+ optional deep dives
- **Sample datasets**: 4 (2 included, 2 available online)
- **Estimated learning time**: 14-15 hours
- **Skill level progression**: Beginner → Advanced

---

## ✅ Quality Checklist

This lab program includes:
- [ ] Working code samples in every notebook
- [ ] Expected outputs shown for verification
- [ ] Troubleshooting guide for each lab
- [ ] Real datasets (not toy examples)
- [ ] Visualization of key concepts
- [ ] Challenge problems for depth
- [ ] Comprehensive setup guide
- [ ] Clear learning objectives
- [ ] Grading rubric for self-assessment
- [ ] Multiple learning paths

---

## 📝 Citation

If you use these labs in your teaching or learning, cite as:

```
RAG Learning Tutorial - Practical Labs
Available at: [your github/documentation URL]
```

---

## 🤝 Contributing

Found a bug? Have a better explanation? Want to add a lab?
- Report issues [here]
- Submit improvements via pull request
- Share your modifications

---

## 📄 License

MIT License - Free for educational and commercial use

---

## 🎯 Your Learning Journey Starts Here

**Ready?** → Start: [Lab 0: Environment Setup](notebooks/lab_0_environment.ipynb)

**Questions?** → Read: [CURRICULUM_GUIDE.md](CURRICULUM_GUIDE.md)

**Installation help?** → Follow: [SETUP.md](SETUP.md)

---

Happy learning! 🚀

--8<-- "_abbreviations.md"
