from typing import List

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from backend.app.graph.state import GraphState
from backend.app.llm.groq_llm import llm_groq
from backend.app.memory.long_term_memory import get_all_memories


# --------------------------------
# Structured Output Schema
# --------------------------------

class TaskSchema(BaseModel):
    tasks: List[str] = Field(
        ...,
        description="A list of clear subtasks to be executed by the worker."
    )


# Make the LLM return structured output
orchestrator_llm = llm_groq.with_structured_output(TaskSchema)


# --------------------------------
# Orchestrator Node
# --------------------------------

def orchestrator_node(state: GraphState) -> GraphState:

    user_query = state["query"]

    # Short-term memory
    chat_history = state.get("chat_history", [])

    # Long-term memory
    user_id = state.get("user_id", "default_user")
    long_term_memory = get_all_memories(user_id)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an AI task orchestrator for a Student Career & Research Assistant.

Your job is to understand the user's current request and break it into
clear, independent subtasks for a worker to execute.

Use both short-term conversation history and long-term user memory
when they are relevant.

Possible task types include:
- web research
- Wikipedia research
- news research
- career or job analysis
- company research
- finance or stock analysis
- calculations
- currency conversion
- Python/data analysis
- PDF/document analysis
- summarization
- learning roadmap creation

Create only the tasks that are necessary.

Each task should:
- be specific
- be clear
- be useful
- be easy for a worker to execute
- avoid unnecessary duplication
"""
            ),
            (
                "user",
                """
Long-term user memory:
{long_term_memory}

Short-term conversation history:
{chat_history}

Current user query:
{query}

Break the current user query into clear subtasks.

Use the long-term memory and conversation history when relevant.
"""
            ),
        ]
    )

    chain = prompt | orchestrator_llm

    response = chain.invoke(
        {
            "query": user_query,
            "chat_history": chat_history,
            "long_term_memory": long_term_memory,
        }
    )

    state["tasks"] = response.tasks

    return state