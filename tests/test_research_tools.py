from backend.app.tools.research_tools import (
    wikipedia_tool,
    duckduckgo_tool,
)


print("\n--- WIKIPEDIA TEST ---")
wiki_result = wikipedia_tool.invoke("Data Science")
print(wiki_result)


print("\n--- WEB SEARCH TEST ---")
search_result = duckduckgo_tool.invoke(
    "current skills required for data scientist jobs"
)
print(search_result)
