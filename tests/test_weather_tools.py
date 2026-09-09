from backend.app.tools.weather_tools import weather_tool


print("\n--- WEATHER TOOL TEST ---")

result = weather_tool.invoke(
    "Kuala Lumpur"
)

print(result)