from backend.app.memory.chat_history import (
    create_conversation,
    save_message,
    get_recent_conversations,
    get_conversation_messages,
)


# --------------------------------
# Test Data
# --------------------------------

thread_id = "test_chat_001"
user_id = "student_001"


# --------------------------------
# Create Conversation
# --------------------------------

print("\n--- CREATE CONVERSATION ---")

create_conversation(
    thread_id=thread_id,
    user_id=user_id,
    title="Data Scientist Career"
)

print("Conversation created successfully.")


# --------------------------------
# Save Messages
# --------------------------------

print("\n--- SAVE MESSAGES ---")

save_message(
    thread_id=thread_id,
    role="user",
    content="I want to become a Data Scientist."
)

save_message(
    thread_id=thread_id,
    role="assistant",
    content="I can help you build a Data Scientist career roadmap."
)

print("Messages saved successfully.")


# --------------------------------
# Recent Conversations
# --------------------------------

print("\n--- RECENT CONVERSATIONS ---")

conversations = get_recent_conversations(
    user_id=user_id
)

for conversation in conversations:
    print(conversation)


# --------------------------------
# Load Conversation Messages
# --------------------------------

print("\n--- CONVERSATION MESSAGES ---")

messages = get_conversation_messages(
    thread_id=thread_id
)

for message in messages:
    print(message)