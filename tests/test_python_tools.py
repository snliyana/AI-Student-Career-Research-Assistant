from backend.app.tools.python_tools import calculator_tool


print("\n--- CALCULATOR TOOL TEST ---")

result = calculator_tool.invoke(
    "125 * 48"
)

print(result)
