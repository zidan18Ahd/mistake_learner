import sys
from pathlib import Path
from pipeline import pipeline, PipelineState
from data_models import CodePair
from storage import store          

def run(wrong_path: str, fixed_path: str, lang: str = "python"):
    wrong_code = Path(wrong_path).read_text(encoding="utf-8")
    fixed_code = Path(fixed_path).read_text(encoding="utf-8")

    state: PipelineState = {
        "code_pair": CodePair(
            wrong_code=wrong_code,
            fixed_code=fixed_code,
            language=lang
        )
    }

    final = pipeline.invoke(state)

    if not final.get("is_real_mistake"):
        print("\n Not a real mistake (probably style/formatting).")
        print("Reason:", final.get("reason", "n/a"))
        return

    print("\n Real mistake detected.")
    print("\n--- Hypothesised WRONG reasoning ---")
    print(final.get("wrong_reasoning", "n/a"))
    print("\n--- CORRECT reasoning ---")
    print(final.get("correct_reasoning", "n/a"))
    print("\n--- DIVERGENCE point (root cause) ---")
    print(final.get("divergence", "n/a"))

    node = final.get("memory_node")
    if node:
        print("\n Memory node ready:")
        print(node.model_dump_json(indent=2))
        store.add(node)                              # ← NEW
        print(f"\n Stored in memory. Total mistakes: {store.count()}")  # ← NEW
    else:
        print("No memory node created.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main_cli.py wrong_code.py fixed_code.py")
        sys.exit(1)
    run(sys.argv[1], sys.argv[2])