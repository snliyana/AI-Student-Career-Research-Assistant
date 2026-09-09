from backend.app.graph.workflow import app_graph
from backend.app.memory.long_term_memory import get_all_memories


user_id = "liyana"


# --------------------------------
# First conversation
# --------------------------------

config_1 = {
    "configurable": {
        "thread_id": "thread_001"
    }
}

state_1 = {
    "query": (
        "I want to become a Machine Learning Engineer "
        "and I prefer hands-on learning."
    ),
    "tasks": [],
    "results": [],
    "summary": "",
    "chat_history": [],
    "user_id": user_id,
}

result_1 = app_graph.invoke(
    state_1,
    config=config_1
)

print("\n--- FIRST RESPONSE ---")
print(result_1["summary"])


# --------------------------------
# Check SQLite directly
# --------------------------------

print("\n--- SAVED LONG-TERM MEMORY ---")
print(get_all_memories(user_id))


# --------------------------------
# Second conversation
# NEW THREAD ID
# --------------------------------

config_2 = {
    "configurable": {
        "thread_id": "thread_002"
    }
}

state_2 = {
    "query": (
        "Create a learning plan for me based on "
        "what you already know about my career goal "
        "and learning preference."
    ),
    "tasks": [],
    "results": [],
    "summary": "",
    "chat_history": [],
    "user_id": user_id,
}

result_2 = app_graph.invoke(
    state_2,
    config=config_2
)

print("\n--- SECOND RESPONSE USING NEW THREAD ---")
print(result_2["summary"])