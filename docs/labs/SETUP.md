# Lab Setup & Installation Guide

Complete step-by-step guide to setting up your RAG learning environment.

## ⚡ Quick Start (5 minutes)

### Use PyCharm

![pyCharm.png](../images/pyCharm.png)


### macOS/Linux
not needed if pycharm or Jupyter nitebooks are used
```bash
# 1. Navigate to lab directory
cd docs/labs

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements-labs.txt

# 4. Verify installation
python -c "from sentence_transformers import SentenceTransformer; print('✅ Ready!')"

# 5. Start Jupyter
jupyter notebook
```

### Windows (Command Prompt)
```bash
cd docs/labs
python -m venv venv
venv\Scripts\activate
pip install -r requirements-labs.txt
python -c "from sentence_transformers import SentenceTransformer; print('✅ Ready!')"
jupyter notebook
```


## 📊 Optional: Advanced Setup

### For Using OpenAI API (Lab 7 optional)
```bash
pip install openai
# Set environment variable:
export OPENAI_API_KEY="your-key-here"
```

### For Using MongoDB Atlas (Full Dataset)
```bash
pip install pymongo  
# Connection string in code: mongodb+srv://user:pass@cluster.mongodb.net/
```

### For GPU Support
```bash
# NVIDIA GPU (CUDA 11.8)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Apple Silicon Mac
conda install pytorch::pytorch torchvision torchaudio -c pytorch
```


## 🆘 Emergency Reset

If something breaks badly:

```bash
# Remove virtual environment
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows command prompt

# Start fresh
python3 -m venv .venv
source .venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements-labs.txt
```

**Setup complete?** Start with [Lab 0: Environment Setup](../notebooks/lab_0_environment.ipynb) 🚀

## Mongo DB

Allow the IP Address of your machine to access the MongoDB Atlas cluster by adding it to the IP Access List in the MongoDB Atlas dashboard.
![allow_ip.png](../images/allow_ip.png)

After the db is set up, you can inspect the search index to see how documents are being chunked and embedded for retrieval.
![search_index.png](../images/search_index.png)

![vector_index.png](../images/vector_index.png)


