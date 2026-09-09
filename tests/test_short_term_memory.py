from backend.app.graph.workflow import app_graph


config = {
    "configurable": {
        "thread_id": "student_001"
    }
}


# First message
state_1 = {
    "query": "My name is Liyana and I want to become a Data Scientist.",
    "tasks": [],
    "results": [],
    "summary": "",
    "chat_history": [],
    "user_id": "liyana",
}

result_1 = app_graph.invoke(
    state_1,
    config=config
)

print("\n--- FIRST RESPONSE ---")
print(result_1["summary"])


# Second message in the SAME thread
state_2 = {
    "query": "What career did I say I want to pursue?",
    "tasks": [],
    "results": [],
    "summary": "",
    "chat_history": [],
    "user_id": "liyana",
}

result_2 = app_graph.invoke(
    state_2,
    config=config
)

print("\n--- SECOND RESPONSE ---")
print(result_2["summary"])