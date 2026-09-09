from backend.app.tools.career_tools import career_job_analysis_tool


print("\n--- CAREER TOOL TEST ---")

result = career_job_analysis_tool.invoke(
    "skills required for Data Scientist"
)

print(result)