from langchain_core.tools import tool

from backend.app.tools.research_tools import duckduckgo_tool


# --------------------------------
# Career Analysis Tool
# --------------------------------

@tool
def career_job_analysis_tool(query: str) -> str:
    """
    Analyze a career or job-related request.

    Example:
    - skills required for Data Scientist
    - technologies commonly required for AI Engineer
    - responsibilities of Machine Learning Engineer
    """

    try:
        return (
            "Career analysis request received: "
            f"{query}. "
            "Use this tool together with web research to identify "
            "required skills, technologies, responsibilities, "
            "and career insights."
        )

    except Exception as e:
        return (
            "Career analysis failed. "
            f"Error: {str(e)}"
        )


# --------------------------------
# Job / Company Search Tool
# --------------------------------

@tool
def job_company_search_tool(query: str) -> str:
    """
    Search for job opportunities, companies, job requirements,
    career roles, and hiring information.

    Examples:
    - Data Scientist jobs in Malaysia
    - companies hiring AI Engineers in Singapore
    - skills required for Machine Learning Engineer
    """

    try:
        search_query = (
            f"jobs careers hiring companies requirements {query}"
        )

        result = duckduckgo_tool.invoke(search_query)

        if not result:
            return "No job or company information was found."

        return result

    except Exception as e:
        return (
            "Job and company search is temporarily unavailable. "
            f"Error: {str(e)}"
        )