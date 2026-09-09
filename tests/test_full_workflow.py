from backend.app.graph.workflow import app_graph


config = {
    "configurable": {
        "thread_id": "full_test_001"
    }
}


initial_state = {
    "query": (
        "I want to become a Data Scientist in Malaysia. "
        "Find the current skills required, search for companies hiring, "
        "compare salary information, and create a short learning roadmap for me."
    ),
    "tasks": [],
    "results": [],
    "summary": "",
    "chat_history": [],
    "user_id": "liyana",
}


result = app_graph.invoke(
    initial_state,
    config=config
)


print("\n--- TASKS ---")

for i, task in enumerate(result["tasks"], start=1):
    print(f"{i}. {task}")


print("\n--- WORKER RESULTS ---")

for i, output in enumerate(result["results"], start=1):
    print(f"\nResult {i}:")
    print(output)


print("\n--- FINAL RESPONSE ---")
print(result["summary"])