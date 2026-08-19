import ast
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def calculate(expression: str):
    """Safely evaluate basic mathematical expressions."""

    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate(tree.body)

        return {
            "success": True,
            "expression": expression,
            "result": result
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Invalid mathematical expression: {str(e)}"
        }


def _evaluate(node):

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)

        operation = OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Unsupported operator")

        return operation(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)

        operation = OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Unsupported operator")

        return operation(operand)

    raise ValueError("Only numbers and basic mathematical operators are allowed")