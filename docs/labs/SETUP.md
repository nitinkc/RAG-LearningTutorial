# Lab Setup & Installation Guide

Complete step-by-step guide to setting up your RAG learning environment.

## ⚡ Quick Start (5 minutes)

### macOS/Linux
```bash
# 1. Navigate to lab directory
cd docs/labs

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

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

---

## 📦 Detailed Installation Guide

### Step 1: Check Python Version
```bash
python --version
# Should be 3.9 or higher
```

If you need Python 3.9+:
- **macOS**: `brew install python@3.11`
- **Windows**: https://www.python.org/downloads/
- **Linux**: `sudo apt-get install python3.11`

### Step 2: Create Virtual Environment

**Why?** Isolates project dependencies, prevents conflicts

```bash
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

# Verify activation (should show "(venv)" in terminal)
which python  # or where python on Windows
```

### Step 3: Upgrade pip

```bash
pip install --upgrade pip
# If issues, try: python -m pip install --upgrade pip
```

### Step 4: Install Core Dependencies

```bash
# Option A: Install everything at once (recommended)
pip install -r requirements-labs.txt

# Option B: Install in stages (if you get errors)
# 1. Data science
pip install numpy pandas scikit-learn scipy matplotlib seaborn

# 2. Embeddings (this downloads ~500MB models)
pip install sentence-transformers torch

# 3. Vector database
pip install chromadb rank-bm25

# 4. Notebooks
pip install jupyter ipykernel ipywidgets
```

### Step 5: Verify Installation

```bash
# Test all imports
python << 'EOF'
import numpy as np
import pandas as pd
import sklearn
from sentence_transformers import SentenceTransformer
import chromadb
from rank_bm25 import BM25Okapi
import matplotlib.pyplot as plt
print("✅ All libraries installed successfully!")
EOF
```

---

## 🚀 Launch Jupyter Notebooks

### Start Jupyter Server
```bash
# Make sure virtual environment is activated
jupyter notebook
```

This opens your browser at `http://localhost:8888`

### Open a Lab Notebook
1. Navigate to: `notebooks/`
2. Click on `lab_0_environment.ipynb`
3. Start from the first cell

### Run a Cell
- Click cell, then press `Shift + Enter`
- Or use the play button in toolbar

---

## ⚙️ Configuration Files

### Python Path Configuration
Add this to `~/.bashrc` or `~/.zshrc` (optional):
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/docs/labs"
```

### Jupyter Configuration (Optional)
```bash
# Create config folder
jupyter --paths

# Customize if needed (advanced)
```

---

## 🛠️ Troubleshooting

### Issue: "Python version not found"
**Solution**: 
```bash
python3 -m venv venv  # Use python3 explicitly
source venv/bin/activate
```

### Issue: "ModuleNotFoundError: No module named 'sentence_transformers'"
**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall
pip install sentence-transformers
```

### Issue: "pip install hangs or is slow"
**Solution**:
```bash
# Use a different package index
pip install -i https://mirrors.aliyun.com/pypi/simple -r requirements-labs.txt
```

### Issue: "CUDA not available" (GPU warning)
**Solution**: This is normal if you don't have NVIDIA GPU. CPU mode is fine for learning.
```bash
# Verify PyTorch can use available devices
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

### Issue: "Port 8888 already in use"
**Solution**:
```bash
# Use different port
jupyter notebook --port 8889

# Or kill existing process
lsof -ti:8888 | xargs kill -9  # macOS/Linux
```

### Issue: Notebook doesn't load kernel
**Solution**:
```bash
# Install kernel for this environment
python -m ipykernel install --user --name rag-labs --display-name "RAG Labs"

# Then select kernel: Kernel → Change Kernel → RAG Labs
```

---

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

---

## ✅ Verification Checklist

- [ ] Python 3.9+ installed
- [ ] Virtual environment created and activated
- [ ] All packages installed without errors
- [ ] `jupyter notebook` starts successfully
- [ ] Can open a lab notebook
- [ ] Can execute cells without import errors
- [ ] Sample embedding creates successfully

---

## 🎯 Recommended Lab Workflow

1. **Activate environment first**:
   ```bash
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

2. **Start Jupyter**:
   ```bash
   jupyter notebook
   ```

3. **Open Lab 0**: `notebooks/lab_0_environment.ipynb`

4. **Run cells sequentially**: Follow the tutorial

5. **Experiment**: Modify code and see what happens

6. **Take notes**: Important insights for each lab

---

## 📚 Next Steps After Setup

1. **Start with Lab 0**: Verify your environment
2. **Progress sequentially**: Each lab builds on previous
3. **Complete exercises**: Don't skip the TODOs
4. **Review expected outputs**: Compare your results
5. **Join community**: Share questions and insights

---

## 💬 Getting Help

### Common Questions

**Q: How much disk space do I need?**
A: ~2GB for all models (BERT embeddings ~500MB)

**Q: Can I work without a GPU?**
A: Yes! CPU is fine for learning. It's just slower.

**Q: How long to complete all labs?**
A: 8-12 hours total, spread over several days recommended

**Q: Can I work online without internet?**
A: After initial setup, mostly yes (except Lab 4 if using MongoDB Atlas)

---

## 🆘 Emergency Reset

If something breaks badly:

```bash
# Remove virtual environment
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows command prompt

# Start fresh
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements-labs.txt
```

---

**Setup complete?** Start with [Lab 0: Environment Setup](../notebooks/lab_0_environment.ipynb) 🚀

--8<-- "_abbreviations.md"
