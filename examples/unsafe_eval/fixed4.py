import ast
import operator

def calculate(expression):
    # Only allow safe math operations
    allowed = {ast.Add: operator.add, ast.Sub: operator.sub,
               ast.Mult: operator.mul, ast.Div: operator.truediv}
    tree = ast.parse(expression, mode="eval")
    return eval(compile(tree, "", "eval"), {"__builtins__": {}}, allowed)