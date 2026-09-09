from backend.app.tools.career_tools import (
    job_company_search_tool,
)


print("\n--- JOB / COMPANY SEARCH TOOL TEST ---")

result = job_company_search_tool.invoke(
    "Data Scientist jobs in Malaysia"
)

print(result)