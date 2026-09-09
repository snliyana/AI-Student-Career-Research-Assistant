from backend.app.tools.news_tools import news_search_tool


print("\n--- NEWS SEARCH TOOL TEST ---")

result = news_search_tool.invoke(
    "Artificial Intelligence jobs"
)

print(result)