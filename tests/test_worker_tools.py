from backend.app.graph.worker import worker_node


state = {
    "query": "",
    "tasks": [
        "Find current skills required for a Data Scientist.",
        "Get stock information for NVIDIA using ticker NVDA.",
        "Calculate 125 * 48.",
        "Convert 1000 USD to MYR.",
        "Get current weather in Kuala Lumpur.",
        "Search for Data Scientist jobs in Malaysia."
    ],
    "results": [],
    "summary": "",
    "chat_history": [],
    "user_id": "liyana",
}


result = worker_node(state)


print("\n--- WORKER TOOL RESULTS ---")

for i, output in enumerate(result["results"], start=1):
    print(f"\nResult {i}:")
    print(output)