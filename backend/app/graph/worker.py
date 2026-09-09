from backend.app.graph.state import GraphState
from backend.app.llm.groq_llm import llm_groq

# Research tools
from backend.app.tools.research_tools import (
    wikipedia_tool,
    duckduckgo_tool,
)

# News
from backend.app.tools.news_tools import news_search_tool

# Finance
from backend.app.tools.finance_tools import stock_info_tool

# Weather
from backend.app.tools.weather_tools import weather_tool

# Calculator
from backend.app.tools.python_tools import calculator_tool

# Currency
from backend.app.tools.currency_tools import currency_converter_tool

# Python / Data Analysis
from backend.app.tools.data_analysis_tools import (
    python_data_analysis_tool,
)

# Career / Job
from backend.app.tools.career_tools import (
    career_job_analysis_tool,
    job_company_search_tool,
)

# PDF
from backend.app.tools.document_tools import pdf_reader_tool


# --------------------------------
# All Worker Tools
# --------------------------------

tools = [
    wikipedia_tool,
    duckduckgo_tool,
    news_search_tool,
    stock_info_tool,
    weather_tool,
    calculator_tool,
    currency_converter_tool,
    python_data_analysis_tool,
    career_job_analysis_tool,
    job_company_search_tool,
    pdf_reader_tool,
]


# Bind tools to Groq LLM
worker_llm = llm_groq.bind_tools(tools)


# --------------------------------
# Tool Executor
# --------------------------------

def execute_tool_call(tool_call):

    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    for tool in tools:

        if tool.name == tool_name:

            try:
                return tool.invoke(tool_args)

            except Exception as e:
                return (
                    f"Tool execution failed for "
                    f"{tool_name}: {str(e)}"
                )

    return f"Tool not found: {tool_name}"


# --------------------------------
# Worker Node
# --------------------------------

def worker_node(state: GraphState) -> GraphState:

    tasks = state["tasks"]

    results = []

    for task in tasks:

        prompt = f"""
You are an AI worker for a Student Career & Research Assistant.

Execute the following task:

{task}

Choose and use an available tool whenever the task requires
external information, calculation, document reading, or data analysis.

Available capabilities:
- Web search
- Wikipedia research
- Recent news search
- Finance and stock information
- Current weather information
- Mathematical calculations
- Currency conversion
- Python/data analysis
- Career analysis
- Job and company search
- PDF/document reading

Tool selection guidelines:
- Use duckduckgo_tool for general current web research.
- Use wikipedia_tool for encyclopedia/background information.
- Use news_search_tool for recent news.
- Use stock_info_tool for stock or company market information.
- Use weather_tool for weather information.
- Use calculator_tool for basic calculations.
- Use currency_converter_tool for currency conversion.
- Use python_data_analysis_tool for simple data analysis.
- Use career_job_analysis_tool for career guidance.
- Use job_company_search_tool for jobs, hiring, and companies.
- Use pdf_reader_tool when a PDF file path is provided.

Keep the result concise and directly relevant to the task.
"""

        response = worker_llm.invoke(prompt)

        # --------------------------------
        # Tool was selected
        # --------------------------------

        if response.tool_calls:

            tool_results = []

            for tool_call in response.tool_calls:

                tool_result = execute_tool_call(
                    tool_call
                )

                tool_results.append(
                    str(tool_result)
                )

            combined_tool_results = "\n\n".join(
                tool_results
            )

            # Prevent very large tool outputs
            if len(combined_tool_results) > 3000:
                combined_tool_results = (
                    combined_tool_results[:3000]
                    + "\n\n[Tool result truncated.]"
                )

            results.append(
                f"Task: {task}\n\n"
                f"Tool Result:\n{combined_tool_results}"
            )

        # --------------------------------
        # No tool required
        # --------------------------------

        else:

            content = response.content

            # Prevent very large direct LLM responses
            if isinstance(content, str) and len(content) > 3000:
                content = (
                    content[:3000]
                    + "\n\n[Worker response truncated.]"
                )

            results.append(content)

    state["results"] = results

    return state