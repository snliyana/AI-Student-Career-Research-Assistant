from langchain_core.tools import tool

from backend.app.tools.research_tools import duckduckgo_tool


@tool
def news_search_tool(query: str) -> str:
    """
    Search for recent news related to a topic, company,
    technology, career field, or industry.
    """

    try:
        news_query = f"latest news {query}"

        result = duckduckgo_tool.invoke(news_query)

        if not result:
            return "No recent news results were found."

        return result

    except Exception as e:
        return (
            "News search is temporarily unavailable. "
            f"Error: {str(e)}"
        )