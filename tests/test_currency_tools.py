from backend.app.tools.currency_tools import currency_converter_tool


print("\n--- CURRENCY CONVERTER TEST ---")

result = currency_converter_tool.invoke(
    "1000 USD TO MYR"
)

print(result)