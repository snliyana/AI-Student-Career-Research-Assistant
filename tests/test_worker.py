from backend.app.graph.orchestrator import orchestrator_node
from backend.app.graph.worker import worker_node


state = {
    "query": (
        "I want to become a Data Scientist. "
        "Find the current skills required and "
        "create a simple learning roadmap."
    ),
    "tasks": [],
    "results": [],
    "summary": "",
    "chat_history": [],
}


state = orchestrator_node(state)

print("\n--- TASKS ---")
for i, task in enumerate(state["tasks"], start=1):
    print(f"{i}. {task}")


state = worker_node(state)

print("\n--- WORKER RESULTS ---")
for i, result in enumerate(state["results"], start=1):
    print(f"\nResult {i}:")
    print(result)