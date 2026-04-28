# Copilot Instructions — MkDocs Documentation Guide

This guide documents best practices, solutions, and configurations learned from building the RAG Learning Tutorial project. It's designed to be reusable for any MkDocs Material theme documentation project, with a dedicated section for RAG-specific customizations.

---

## PART 1: REUSABLE MKDOCS CONFIGURATION GUIDE

### Project Structure

```
project-name/
├── mkdocs.yml                    ← Master configuration
├── requirements.txt              ← Python dependencies
├── README.md                     ← Project overview
├── docs/
│   ├── index.md                  ← Home page
│   ├── _abbreviations.md         ← Glossary definitions
│   ├── css/
│   │   └── extra.css             ← Custom styling
│   ├── js/
│   │   ├── mathjax.js            ← Math config
│   │   ├── mermaid-init.js       ← Diagram config
│   │   ├── theme-toggle.js       ← Theme persistence
│   │   └── [other scripts]
│   └── [section folders]/
│       └── *.md files
├── site/                         ← Generated output
└── .venv/                        ← Python virtual env
```

### Essential Dependencies

```
mkdocs>=1.5.0
mkdocs-material>=9.5.0
pymdown-extensions>=10.8
Markdown>=3.6
```

### Core Configuration Pattern (mkdocs.yml)

Key sections:
- **theme**: Material with palette for light/dark modes
- **plugins**: search (minimal)
- **markdown_extensions**: superfences, highlight, details, arithmatex, abbr
- **extra_javascript**: mathjax config, mathjax library, mermaid, mermaid-init, theme-toggle
- **extra_css**: extra.css for custom styling

---

## PART 2: KNOWN ISSUES & SOLUTIONS

### Issue 1: Markdown Lists Not Rendering

**Problem:** Lists appear as plain text instead of formatted lists when there's no blank line before them.

**Root Cause:** Markdown parsers require a blank line between body text and list items.

**Solution:**
```markdown
✅ CORRECT:
Some text

- List item 1
- List item 2
```

---

### Issue 2: Mermaid Diagrams Not Rendering

**Problem:** Mermaid code blocks appear as highlighted code instead of rendered diagrams.

**Root Cause:** Custom Python fence configuration caused module import errors. Solution: use client-side JavaScript.

**Files to Create/Update:**

1. `docs/js/mermaid-init.js` - Converts code blocks to mermaid divs and initializes library
2. `mkdocs.yml` - Add to extra_javascript:
   - `https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js`
   - `js/mermaid-init.js`

**Key Code:**
```javascript
// Detect mermaid in code blocks and convert to divs
if (text.startsWith('graph ') || text.includes('graph LR')) {
  const mermaidDiv = document.createElement('div');
  mermaidDiv.className = 'mermaid';
  mermaidDiv.textContent = text;
  highlightDiv.replaceWith(mermaidDiv);
}
```

---

### Issue 3: Math Equations Not Rendering

**Problem:** Math equations appear as LaTeX code instead of rendered equations.

**Root Cause:** Incorrect JavaScript loading order (config must load BEFORE library).

**Files to Create/Update:**

1. `docs/js/mathjax.js` - Contains MathJax configuration
2. `mkdocs.yml` - Correct order in extra_javascript:
   ```yaml
   - js/mathjax.js                # Config FIRST
   - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js  # Library SECOND
   ```

3. `mkdocs.yml` - markdown_extensions:
   ```yaml
   - pymdownx.arithmatex:
       generic: true
       block_tag: 'div'
   ```

**Critical:** Load order is essential!

---

### Issue 4: Collapsible Sections Not Working

**Problem:** HTML `<details>` tags appear as plain text instead of collapsible sections.

**Root Cause:** Missing CSS styling.

**Solution:**

1. Add to `docs/css/extra.css`:
```css
details {
  margin: 1.5em 0;
  padding: 0.5em 0;
  border-left: 4px solid [theme-color];
  padding-left: 1em;
}

details summary {
  cursor: pointer;
  font-weight: 600;
  color: [theme-color];
  user-select: none;
  outline: none;
  padding: 0.5em 0;
}

details summary:hover {
  color: [lighter-color];
}

/* Dark mode support */
[data-md-color-scheme="slate"] details {
  border-left-color: [dark-color];
}

[data-md-color-scheme="slate"] details summary {
  color: [dark-color];
}

[data-md-color-scheme="slate"] details summary:hover {
  color: [bright-color];
}
```

2. In Markdown:
```markdown
<details>
<summary>Click to expand</summary>

Your content here

</details>
```

---

### Issue 5: Glossary/Abbreviations Not Rendering

**Problem:** Glossary terms don't show underlines, and definitions aren't visible on hover.

**Root Cause:** Missing `_abbreviations.md` file or abbreviation syntax not configured.

**Solution:**

1. Create `docs/_abbreviations.md`:
```markdown
*[ACRONYM]: Full expansion text
*[API]: Application Programming Interface
```

2. Include at bottom of markdown files:
```markdown
--8<-- "_abbreviations.md"
```

3. `mkdocs.yml` should have:
```yaml
markdown_extensions:
  - abbr
  - pymdownx.snippets  # Enables --8<-- inclusion
```

4. Optional CSS for hover styling:
```css
abbr[title] {
  text-decoration: underline dotted;
  cursor: help;
}
```

**Note:** Must include `--8<-- "_abbreviations.md"` in each file where abbreviations appear.

---

## PART 3: THEME CUSTOMIZATION GUIDE

### Implementing Dark & Light Theme Toggle

**Implementation:**

1. `mkdocs.yml` palette section:
```yaml
theme:
  palette:
    - scheme: default
      primary: [color]
      accent: [color]
      toggle:
        icon: material/weather-night
        name: Switch to dark mode
    - scheme: slate
      primary: [color]
      accent: [color]
      toggle:
        icon: material/weather-sunny
        name: Switch to light mode
```

2. Create `docs/js/theme-toggle.js` to persist user preference

3. Add to `extra_javascript` in mkdocs.yml

---

## PART 4: BEST PRACTICES

- **Lists:** Always add blank line before lists
- **Code:** Use collapsible `<details>` for long examples
- **Math:** Test equation rendering on both themes
- **Navigation:** Link between related sections, add "Next Steps"
- **Build:** Always run `mkdocs build` to catch errors early

---

## PART 5: BUILD & DEPLOYMENT

```bash
mkdocs serve          # Local development (http://localhost:8000)
mkdocs build          # Build static site (output in site/)
mkdocs build -f mkdocs.yml  # Explicit config
```

---

## PART 6: RAG PROJECT SPECIFIC CONFIGURATION

### Project: RAG Learning Tutorial

**Purpose:** Math-first guide to Retrieval-Augmented Generation from first principles to production.

**Core Narrative:** Solving the "Order #1766 vs Order #1767" exact match problem through hybrid search.

### Custom Color Scheme (Teal Theme)

**Light Mode:**
- Primary: `#00897b` (Deep Teal)
- Accent: `#00bfa5` (Bright Teal)

**Dark Mode (Slate):**
- Primary: `#4db6ac` (Bright Teal)
- Accent: `#64ffda` (Vivid Cyan)
- Background: `#1a1a2e`

Apply in `mkdocs.yml`:
```yaml
theme:
  palette:
    - scheme: default
      primary: teal
      accent: teal
    - scheme: slate
      primary: teal
      accent: teal
```

### Navigation Structure (5 Main Sections)

```
00 · Prerequisites (Math foundations)
01 · Understanding Embeddings
02 · Similarity Search
03 · Retrieval Methods (Dense, Sparse, Hybrid)
04 · Exact Match Problem (Core challenge)
05 · RAG Pipeline (Complete system)
```

### RAG-Specific Content Guidelines

1. **Mathematical Rigor**
   - Always show derivations with intuitive explanations
   - Use inline math: `$equation$`
   - Use display math: `$$equation$$`
   - Include Python code alongside theory

2. **Practical Examples**
   - Real library names (SentenceTransformer, Qdrant, BM25Okapi)
   - Working code snippets
   - Expected output/results
   - Use collapsible `<details>` for long code

3. **Mermaid Diagrams**
   - Pipeline architectures
   - Data flow diagrams
   - Problem visualization
   - Decision trees

4. **Progressive Complexity**
   - Start with intuition
   - Build to mathematical derivation
   - End with practical implementation
   - Use "Next Steps" links

### RAG-Specific Abbreviations

```markdown
*[RAG]: Retrieval-Augmented Generation
*[BM25]: Okapi BM25 ranking function
*[HNSW]: Hierarchical Navigable Small World
*[TF-IDF]: Term Frequency-Inverse Document Frequency
*[LLM]: Large Language Model
*[MRR]: Mean Reciprocal Rank
*[IDF]: Inverse Document Frequency
*[RRF]: Reciprocal Rank Fusion
*[ANN]: Approximate Nearest Neighbor
*[BERT]: Bidirectional Encoder Representations from Transformers
*[IVF]: Inverted File Index
```

### File Organization Pattern

```
docs/
├── index.md                 # Learning path + architecture
├── 00-prerequisites/
│   ├── index.md            # Math overview
│   ├── linear-algebra.md   # Vectors, products, norms
│   └── probability-stats.md
├── 01-embeddings/
│   ├── index.md
│   ├── what-are-embeddings.md
│   ├── embedding-models.md
│   └── vector-spaces.md
├── [other sections...]
└── _abbreviations.md       # Glossary
```

---

## PART 7: TROUBLESHOOTING CHECKLIST

When regenerating documentation:

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Test build: `mkdocs build` (no errors)
- [ ] Verify list formatting (blank lines)
- [ ] Check Mermaid rendering (mermaid-init.js loaded)
- [ ] Test math equations (load order correct)
- [ ] Verify collapsible sections (CSS present)
- [ ] Test glossary (abbreviations included)
- [ ] Toggle themes (theme-toggle.js working)
- [ ] Mobile responsive
- [ ] Search functionality working

---

## QUICK REFERENCE: Color Mapping

For new color schemes, replace these values:

**In mkdocs.yml:**
- `primary: teal` → change to desired color
- `accent: teal` → change to desired color

**In docs/css/extra.css:**
- `#00897b` → Light theme primary
- `#4db6ac` → Dark theme primary
- `#00bfa5` → Light theme accent
- `#64ffda` → Dark theme accent

---

**Version:** 2.0  
**Last Updated:** April 28, 2026  
**Created From:** RAG Learning Tutorial project  
**Reusable:** Yes - PART 1-5 are general purpose, PART 6-7 are RAG-specific  
**Status:** Production Ready ✅

