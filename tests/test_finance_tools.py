from backend.app.tools.finance_tools import stock_info_tool


print("\n--- FINANCE TOOL TEST ---")

result = stock_info_tool.invoke("NVDA")

print(result)