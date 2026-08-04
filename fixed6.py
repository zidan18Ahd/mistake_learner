import ast
def run_math(expression):
    allowed = {"abs": abs, "round": round}
    return eval(expression, {"__builtins__": {}}, allowed)