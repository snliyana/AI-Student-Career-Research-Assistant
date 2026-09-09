import ast

from langchain_core.tools import tool


@tool
def python_data_analysis_tool(code: str) -> str:
    """
    Execute simple Python data analysis code.

    Useful for:
    - averages
    - totals
    - percentages
    - simple statistics
    - list-based calculations

    Example:
    sum([10, 20, 30]) / 3
    """

    try:
        tree = ast.parse(code, mode="eval")

        allowed_nodes = (
            ast.Expression,
            ast.Constant,
            ast.List,
            ast.Tuple,
            ast.Dict,
            ast.Set,
            ast.BinOp,
            ast.UnaryOp,
            ast.Add,
            ast.Sub,
            ast.Mult,
            ast.Div,
            ast.Mod,
            ast.Pow,
            ast.USub,
            ast.UAdd,
            ast.Call,
            ast.Name,
            ast.Load,
        )

        for node in ast.walk(tree):
            if not isinstance(node, allowed_nodes):
                return "Unsupported Python expression."

        allowed_functions = {
            "sum": sum,
            "min": min,
            "max": max,
            "len": len,
            "round": round,
            "sorted": sorted,
        }

        result = eval(
            compile(tree, "<string>", "eval"),
            {"__builtins__": {}},
            allowed_functions,
        )

        return f"Result: {result}"

    except Exception as e:
        return (
            "Python data analysis failed. "
            f"Error: {str(e)}"
        )