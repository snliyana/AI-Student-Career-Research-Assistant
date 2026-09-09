from backend.app.graph.workflow import app_graph


initial_state = {
    "query": (
        "I want to become a Data Scientist. "
        "Find the current skills required, "
        "identify companies hiring, "
        "compare salary ranges, "
        "analyze required technologies, "
        "and create a learning roadmap."
    ),
    "tasks": [],
    "results": [],
    "summary": "",
    "chat_history": [],
}


result = app_graph.invoke(initial_state)


print("\n--- TASKS ---")
for i, task in enumerate(result["tasks"], start=1):
    print(f"{i}. {task}")


print("\n--- FINAL RESPONSE ---")
print(result["summary"])