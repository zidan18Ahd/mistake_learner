# Mistake Learner – Personal AI Code Reviewer

A CLI tool that goes beyond traditional code linting by learning your personal reasoning mistakes over time.

Instead of only identifying bugs, it tries to understand *why* you made the mistake. For example, instead of simply reporting an SQL injection vulnerability, it may infer that you assumed user input would always be safe. Each reasoning mistake is stored as a semantic memory, allowing the system to build a long-term profile of your recurring coding blind spots.

Over time, these memories form an interactive graph that helps you visualize and understand your personal reasoning patterns.

---

# Features

- Five-stage LangGraph pipeline for mistake analysis.
- Infers the incorrect reasoning behind a bug.
- Infers the correct reasoning that should have been used.
- Identifies the divergence point between wrong and correct thinking.
- Stores every reasoning mistake in ChromaDB for long-term memory.
- Uses Groq's Llama 3.3 70B model for reasoning.
- Automatically removes duplicate memories.
- Generates an interactive HTML graph of reasoning clusters.

---

# Pipeline

The project follows a five-stage workflow:

1. Code Evaluation
   - Compares the incorrect and corrected versions of the code.

2. Wrong Reasoning Inference
   - Infers the assumption or reasoning that caused the bug.

3. Correct Reasoning Inference
   - Infers the reasoning that would have prevented the mistake.

4. Divergence Detection
   - Identifies where the wrong reasoning diverged from the correct reasoning.

5. Memory Creation
   - Stores the divergence as a semantic memory in ChromaDB.

---

# Tech Stack

- Python 3.11
- LangGraph
- Groq API
- Llama 3.3 70B
- ChromaDB
- Pyvis
- NetworkX
- Sentence Transformers

---

# Project Structure

```text
mistake_learner/
│
├── main_cli.py
├── visualize.py
├── graph.py
├── state.py
├── prompts.py
├── memory.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
└── chroma_data/
```

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/your-username/mistake_learner.git
cd mistake_learner
```

## 2. Create a virtual environment

### Windows

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Create a `.env` file

Create a file named `.env` in the project root.

```text
GROQ_API_KEY=your_groq_api_key
```

---

# Running the Project

## Analyze a coding mistake

```bash
python main_cli.py wrong.py fixed.py
```

Where:

- `wrong.py` contains the buggy implementation.
- `fixed.py` contains the corrected implementation.

After execution, the program:

- Evaluates both versions.
- Infers your reasoning.
- Stores the mistake.
- Prints the total number of stored memories.

---

## Visualize the reasoning graph

```bash
python visualize.py
```

This generates:

```text
mistake_map.html
```

Open the HTML file in your browser to explore your reasoning graph.
![Mistake Clusters](assets/mistake_clusters.png)
---

# Example Memory

Wrong reasoning:

> "I assumed user input would always be trusted."

Correct reasoning:

> "Any external input should be treated as untrusted and parameterized."

Divergence:

> "Assumed trusted input instead of validating user-controlled data."

This semantic memory becomes part of your personal reasoning database.

---

# Example Graph Clusters

After several runs, the graph may naturally organize into clusters such as:

- SQL Injection
- Resource Management
- Mutable Default Arguments
- Unsafe Eval
- Exception Handling
- File Handling
- Concurrency Mistakes
- State Management

Hover over any node to view the stored reasoning, and drag nodes to explore relationships.

---

# Requirements

If you make changes to dependencies, regenerate the requirements file:

```bash
pip freeze > requirements.txt
```

---

# Git Ignore

A recommended `.gitignore`:

```gitignore
venv/
__pycache__/
*.pyc

.env

chroma_data/

mistake_map.html

.idea/
.vscode/
```

---

# Future Improvements

- Retrieval-Augmented Memory
- Similar mistake recommendations
- Web dashboard
- Automatic GitHub code review integration
- Multi-language support
- Personal learning analytics
- Timeline of reasoning improvements

---

# License

This project is licensed under the MIT License.
