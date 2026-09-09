from backend.app.graph.orchestrator import orchestrator_node
from backend.app.graph.worker import worker_node
from backend.app.graph.collector import collector_node


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
state = worker_node(state)
state = collector_node(state)


print("\n--- FINAL RESPONSE ---")
print(state["summary"])