import wikipedia

from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import (
    WikipediaQueryRun,
    DuckDuckGoSearchRun,
)

from langchain_core.tools import tool


# Wikimedia requires a descriptive User-Agent
wikipedia.set_user_agent(
    "AIStudentCareerResearchAssistant/1.0 (educational project)"
)


# -----------------------------
# Wikipedia Tool
# -----------------------------

wikipedia_wrapper = WikipediaAPIWrapper(
    top_k_results=2,
    doc_content_chars_max=2000
)

wikipedia_tool = WikipediaQueryRun(
    api_wrapper=wikipedia_wrapper
)


# -----------------------------
# Web Search Tool
# -----------------------------

_raw_duckduckgo = DuckDuckGoSearchRun()


@tool
def duckduckgo_tool(query: str) -> str:
    """
    Search the web using DuckDuckGo.
    Returns a safe fallback message if the search fails.
    """

    try:
        result = _raw_duckduckgo.run(query)

        if not result:
            return "Web search returned no results."

        return result

    except Exception as e:
        return (
            "Web search is temporarily unavailable. "
            f"Error: {str(e)}"
        )