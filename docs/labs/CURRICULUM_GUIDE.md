# Lab Curriculum Guide

## Welcome to RAG Learning Labs!

This guide explains the structure, progression, and best practices for working through the RAG labs. It's designed as a **college-level academic program** that teaches RAG from first principles to production systems.

---

## Why These 8 Labs?

The labs are designed with **incremental learning** in mind:

### Foundation Block (Labs 0-2): "Understanding Vectors"
- **Lab 0**: Setup your tools
- **Lab 1**: Build vector math from scratch
- **Lab 2**: See embeddings in action

*Goal*: Deep intuition for how embeddings work

### Database & Ingestion Block (Labs 3-4): "Data Management"
- **Lab 3**: Learn vector database operations
- **Lab 4**: Ingest real data at scale

*Goal*: Understand data persistence and retrieval

### Problem & Solution Block (Labs 5-6): "The Exact Match Problem"  
- **Lab 5**: Discover the core limitation
- **Lab 6**: Implement the solution

*Goal*: Solve the "Order #1766 vs #1767" problem

### Integration Block (Lab 7): "Complete System"
- **Lab 7**: Build end-to-end RAG pipeline

*Goal*: Understand full production system

---

## Learning Time Estimate

| Lab | Time | Difficulty | Focus |
|-----|------|-----------|-------|
| Lab 0 | 30 min | ⭐ | Setup |
| Lab 1 | 1.5 hrs | ⭐⭐ | Math |
| Lab 2 | 1.5 hrs | ⭐⭐ | Embeddings |
| Lab 3 | 2 hrs | ⭐⭐ | Databases |
| Lab 4 | 2.5 hrs | ⭐⭐⭐ | Ingestion |
| Lab 5 | 2 hrs | ⭐⭐⭐ | Problem-Solving |
| Lab 6 | 2.5 hrs | ⭐⭐⭐ | Advanced |
| Lab 7 | 3 hrs | ⭐⭐⭐⭐ | Integration |
| **Total** | **14-15 hrs** | - | - |

**Recommendation**: Spread over 2-3 weeks (1 lab per session)

---

## Prerequisites Check

Before starting, you should have:

- ✅ Python 3.9+ installed (`python --version`)
- ✅ Familiar with Python basics (variables, functions, loops)
- ✅ Understand statistics basics (mean, variance, correlation)
- ✅ Read [RAG Learning Tutorial Prerequisites](../00-prerequisites/index.md)
- ✅ ~2GB free disk space

**Not needed** (don't worry if you don't know):
- ❌ GPU (CPU is fine)
- ❌ Previous ML experience
- ❌ Linear algebra mastery (we teach it in Lab 1)

---

## How to Work Through a Lab

### Pre-Lab (5 min)
1. Read the lab objectives at the top
2. Review "What You'll Learn" section
3. Skim through all cells to see what's coming

### During Lab (Follow the cells)
1. **Code cells**: Run in order using Shift+Enter
2. **Markdown cells**: Read carefully, understand concepts
3. **Exercises**: Modify and experiment with the code
4. **Challenges**: Optional, but highly rewarding

### Post-Lab (10 min)
1. Review the Summary section
2. Try one Challenge exercise
3. Note down key insights
4. Take a screenshot of final results

---

## Pro Tips for Maximum Learning

### 🎯 Tip 1: Don't Just Run Cells
**Don't**: Click play and watch output  
**Do**: Read code, predict output, run, compare

```python
# Bad: Just run this
result = 1 + 1

# Good: Predict first
# I think this will print 2
result = 1 + 1
print(result)  # Verify your prediction
```

### 🎯 Tip 2: Modify and Experiment
```python
# After running the cell:
# Try different values:
# - Change corpus length
# - Change similarity threshold
# - Add new documents
# - See what breaks!
```

### 🎯 Tip 3: Take Notes on Paper
- Key formulas
- When to use which metric
- Common mistakes
- Real-world applications

### 🎯 Tip 4: The "Teach Someone Else" Test
After each lab:
- Explain concept to friend/rubber duck
- Can you explain in 2 minutes?
- If stuck, rewatch relevant sections

### 🎯 Tip 5: Build Your Own Dataset
Instead of just using provided data:
- Lab 4: Add your own documents
- Lab 6: Test with your domain data
- Lab 7: Build for YOUR use case

---

## Common Mistakes to Avoid

### ❌ Skipping Labs 0-1
**Why it matters**: Lab 1 builds intuition you'll need for everything else  
**Solution**: Don't skip! Lab 1 takes 1.5 hours but saves you time later

### ❌ Not Installing Dependencies First
**Why it matters**: Code won't run without proper setup  
**Solution**: Follow [Setup Guide](./SETUP.md) carefully

### ❌ Running Lab 4 Without MongoDB or JSON
**Why it matters**: Lab 4 needs actual data  
**Solution**: The `docs/labs/data/` folder has sample files ready to use

### ❌ Jumping to Lab 7 First
**Why it matters**: Lab 7 assumes you know all previous concepts  
**Solution**: Go sequentially, or use "Accelerated Track" (skip Labs 1-2)

### ❌ Only Reading Without Coding
**Why it matters**: Passive reading doesn't stick  
**Solution**: Code along every example

---

## Multiple Learning Paths

Choose based on YOUR background:

### Path A: "Complete Foundation" (Recommended for beginners)
```
Lab 0 → Lab 1 → Lab 2 → Lab 3 → Lab 4 → Lab 5 → Lab 6 → Lab 7
```
- **Time**: 14-15 hours
- **Best for**: Complete understanding
- **Prerequisite**: Basic Python knowledge

### Path B: "Accelerated" (For ML-familiar learners)
```
Lab 0 → Lab 3 → Lab 4 → Lab 5 → Lab 6 → Lab 7
```
- **Time**: 11-12 hours
- **Skip**: Vector math (assumption: you know it)
- **Note**: Read Lab 1 summary before Lab 3

### Path C: "Problem-Focused" (For specific issues)
```
Lab 0 → Lab 2 → Lab 4 → Lab 5 → Lab 6
```
- **Time**: 9-10 hours
- **Focus**: Solve exact match problem specifically
- **Best for**: Production system issues

### Path D: "Deep Dive Math" (For theory-first learners)
```
Lab 0 → Lab 1 → Lab 2 → Lab 3 → Lab 6 → Lab 7
```
- **Time**: 12-13 hours
- **Skip**: Lab 4, 5 (ingestion and problem specifics)
- **Best for**: Understanding the algorithm

---

## When You Get Stuck

### Level 1: Self-Help
1. **Reread the relevant cell** (understanding > guessing)
2. **Modify the code** slightly and rerun
3. **Check error message** carefully
4. **Google the full error** message
5. **Try the Troubleshooting section** at lab end

### Level 2: Debug Systematically
```python
# Add print statements to see what's happening
print(f"Input: {input_data}")
print(f"Type: {type(input_data)}")
result = function(input_data)
print(f"Output: {result}")
```

### Level 3: Review Prerequisites
- Go back to theory section that explains this
- Read the Reference docs
- Compare with Lab X that used similar concept

### Level 4: Simplify Test Case
```python
# If this fails:
complex_data_result = search_database(complex_corpus, "complex query")

# Try this simpler version:
simple_data = ["cat", "dog", "bird"]
simple_result = search_database(simple_data, "animal")
```

---

## Checkpoint Checklist

After each lab, verify you can:

### Lab 0
- [ ] Import all libraries without errors
- [ ] Run sample embedding code
- [ ] Understand the basic search flow

### Lab 1
- [ ] Implement dot product manually
- [ ] Explain cosine similarity
- [ ] Identify when each distance metric is useful

### Lab 2
- [ ] Generate embeddings for sample text
- [ ] Find similar documents
- [ ] Understand embedding dimensions

### Lab 3
- [ ] Create a Chroma collection
- [ ] Add documents with metadata
- [ ] Perform similarity search
- [ ] Understand HNSW indexing

### Lab 4
- [ ] Load JSON data successfully
- [ ] Implement chunking strategy
- [ ] Ingest 100+ documents efficiently
- [ ] Search across ingested data

### Lab 5
- [ ] Reproduce the exact match problem
- [ ] Visualize why semantic search fails
- [ ] Identify failure cases in your domain

### Lab 6
- [ ] Implement BM25 scoring
- [ ] Combine dense + sparse results
- [ ] Compare hybrid vs semantic search
- [ ] Measure improvement with metrics

### Lab 7
- [ ] Build complete RAG pipeline
- [ ] Evaluate retrieval quality
- [ ] Optimize performance
- [ ] Document your system

---

## Grading Yourself

Labs are self-graded. Evaluate based on:

1. **Correctness (50%)**: Does it work?
2. **Understanding (25%)**: Can you explain?
3. **Analysis (15%)**: Did you learn insights?
4. **Experimentation (10%)**: Did you try variations?

**You passed if**:
- ✅ Code runs without errors
- ✅ You understand why it works
- ✅ You modified and experimented
- ✅ You can answer challenge questions

---

## After Completing Labs

### Next Steps
1. **Build a project**: Apply labs to your data
2. **Explore variations**: Try different embeddings, databases
3. **Read research**: Papers on RAG, embeddings, search
4. **Join community**: Share your insights
5. **Scale up**: Production considerations

### Recommended Next Learning
1. Implement RAG with [LangChain](https://langchain.readthedocs.io/)
2. Learn [LLM integration](../05-rag-pipeline/generation.md)
3. Study [advanced chunking](../04-exact-match/chunking-strategies.md)
4. Explore [production optimization](../05-rag-pipeline/evaluation.md)

---

## Resources by Lab

| Lab | Key File | Concept |
|-----|----------|---------|
| Lab 0 | SETUP.md | Installation |
| Lab 1 | Linear Algebra essentials | Vectors |
| Lab 2 | Embedding models guide | BERT, Sentence-BERT |
| Lab 3 | Vector databases guide | HNSW, indexing |
| Lab 4 | MongoDB datasets | Ingestion pipelines |
| Lab 5 | Exact match problem | Limitations |
| Lab 6 | Hybrid search guide | BM25, RRF |
| Lab 7 | RAG pipeline overview | Complete system |

---

## Hardware & Performance

### Minimum Requirements
- **CPU**: Intel/AMD/Apple Silicon (modern enough to run Python 3.9)
- **RAM**: 4GB (8GB recommended)
- **Storage**: 2GB
- **GPU**: Not needed (but nice to have)

### Performance Expectations
- **Lab 0-2**: < 1 second per cell
- **Lab 3**: ~2-5 seconds for search
- **Lab 4**: 30-60 seconds for ingestion
- **Lab 5**: < 5 seconds per query
- **Lab 6**: 5-10 seconds for hybrid ranking
- **Lab 7**: 1-2 minutes for full pipeline

*If much slower*: Check for CPU intensity, reduce dataset size, try CPU-optimized settings.

---

## Community & Support

### Where to Share
- Document your journey
- Share insights learned
- Post interesting findings
- Ask questions

### What Good Notes Look Like
```markdown
## Lab 3 Insights
- HNSW with M=16 was faster than default
- Adding metadata increased query time by 5%
- Similarity scores in range [0.3, 0.8] for restaurant data
```

---

## FAQ

**Q: Can I skip a lab?**  
A: For paths other than "Complete Foundation", yes. But read the lab summary.

**Q: How often should I take breaks?**  
A: Every 60 minutes. Step away from screen, move around.

**Q: Can I use different libraries (Pinecone, Weaviate)?**  
A: Yes! The concepts apply. Adjust imports/syntax for your library.

**Q: What if I disagree with the approach?**  
A: Great! Test your approach and document findings.

**Q: Should I attend lectures?**  
A: These labs ARE the core content. Consider them as "lecture + homework".

---

## Reflection Template

After completing all labs, reflect:

```
## Completed RAG Learning Labs! 

### What Was Hardest?
[Share your biggest challenge]

### What Clicked the Most?
[Most surprising insight]

### Your Main Takeaway?
[The one thing you'll remember]

### How Would You Explain RAG to a Friend?
[In 3 sentences]

### What Would You Build Next?
[Your RAG application idea]
```

---

## 🎓 Congratulations!

By completing these labs, you now understand:

✅ How vectors represent meaning  
✅ Why cosine similarity works for embeddings  
✅ How vector databases store and search efficiently  
✅ How to ingest real data at scale  
✅ Why semantic search fails for exact matches  
✅ How hybrid search solves real problems  
✅ How to build production RAG systems  
✅ How to evaluate and optimize search  

**You're ready to build intelligent search systems!**

---

**Ready to start?** → [Lab 0: Environment Setup](notebooks/lab_0_environment.ipynb)

--8<-- "_abbreviations.md"
