from backend.app.graph.orchestrator import orchestrator_node


state = {
    "query": (
        "I want to become a Data Scientist. "
        "Find the current skills required, "
        "search for relevant companies, "
        "compare salary ranges, "
        "analyze required technologies, "
        "and create a learning roadmap."
    ),
    "tasks": [],
    "results": [],
    "summary": "",
    "chat_history": [],
}


result = orchestrator_node(state)

print("\n--- ORCHESTRATOR RESULT ---")
for i, task in enumerate(result["tasks"], start=1):
    print(f"{i}. {task}")