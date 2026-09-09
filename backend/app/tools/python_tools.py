from langchain_core.tools import tool


@tool
def calculator_tool(expression: str) -> str:
    """
    Evaluate a basic mathematical expression.

    Example:
    125 * 48
    (1000 * 0.15) + 50
    """

    try:
        allowed_chars = set(
            "0123456789+-*/().% "
        )

        if not set(expression).issubset(allowed_chars):
            return (
                "Invalid expression. "
                "Only numbers and basic mathematical operators are allowed."
            )

        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return f"Result: {result}"

    except Exception as e:
        return (
            "Calculation failed. "
            f"Error: {str(e)}"
        )