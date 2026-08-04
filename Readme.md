arkdown
# Mistake Learner – Personal AI Code Reviewer

A CLI tool that does not just lint your code, but learns your personal reasoning blind spots over time.

Instead of saying "you missed a parameterized query", it figures out why you made that mistake (for example, "you assumed the input would always be safe") and stores that reasoning in a vector database. Over time, it builds a visual "brain map" of your recurring coding weaknesses.

## Features

- 5-Stage LangGraph Pipeline: Evaluates, infers wrong reasoning, infers correct reasoning, finds the divergence point, and builds a memory node.
- Persistent Memory: Stores every mistake in ChromaDB for long-term learning.
- Groq Integration: Uses Llama 3.3 70B (fast and free) to reason about your code.
- Visualization: Generates an interactive HTML graph showing your mistake clusters and semantic similarities.
- Deduplication: Automatically removes duplicate entries so your graph stays clean.

## Tech Stack

- Python 3.11
- LangGraph (StateGraph)
- Groq (Llama 3.3 70B)
- ChromaDB (Vector Database)
- Pyvis / NetworkX (Graph Visualization)

## Setup

1. Clone the repository:
git clone <your-repo-url>
cd mistake_learner

text

2. Create a virtual environment:
- On Windows:
python -m venv venv
.\venv\Scripts\Activate.ps1

text
- On macOS / Linux:
python -m venv venv
source venv/bin/activate

text

3. Install dependencies:
pip install -r requirements.txt

text

4. Set up your Groq API key:
Create a `.env` file in the root directory and add:
GROQ_API_KEY=your_api_key_here

text

## How to Run

1. Analyze a mistake:
python main_cli.py wrong.py fixed.py

text
(Where `wrong.py` has the bug and `fixed.py` has the correction.)

2. Visualize your mistake clusters:
python visualize.py

text
This generates `mistake_map.html`. Open it in your browser to see the interactive graph.

3. View total stored mistakes:
The CLI prints the total count after each run.

## Example Output

After running several examples, the graph shows clusters such as:

- SQL Injection and Resource Leaks (e.g., assuming the connection auto-closes)
- Mutable Default Arguments (e.g., assuming default args are re-created each call)
- Unsafe Eval (e.g., assuming user input is always safe)

Hover over any node to see the full divergence point, and drag nodes apart to explore connections.

## Requirements File

If you do not have a `requirements.txt` yet, generate it by running:
pip freeze > requirements.txt

text

## License

MIT