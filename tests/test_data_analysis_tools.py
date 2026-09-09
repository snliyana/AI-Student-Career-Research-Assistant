from backend.app.tools.data_analysis_tools import (
    python_data_analysis_tool,
)


print("\n--- PYTHON DATA ANALYSIS TOOL TEST ---")

result = python_data_analysis_tool.invoke(
    "round(sum([70, 80, 90, 100]) / 4, 2)"
)

print(result)