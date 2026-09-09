from backend.app.memory.long_term_memory import (
    save_memory,
    get_memory,
    get_all_memories,
)


user_id = "liyana"


print("\n--- SAVE MEMORY ---")

save_memory(
    user_id,
    "career_goal",
    "Data Scientist"
)

save_memory(
    user_id,
    "learning_style",
    "Hands-on projects"
)


print("\n--- GET SINGLE MEMORY ---")

career_goal = get_memory(
    user_id,
    "career_goal"
)

print("Career Goal:", career_goal)


print("\n--- GET ALL MEMORIES ---")

memories = get_all_memories(
    user_id
)

print(memories)