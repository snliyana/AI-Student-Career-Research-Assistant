from typing import Optional

from pydantic import BaseModel, Field

from backend.app.graph.state import GraphState
from backend.app.llm.groq_llm import llm_groq
from backend.app.memory.long_term_memory import save_memory


# --------------------------------
# Memory Extraction Schema
# --------------------------------

class MemorySchema(BaseModel):
    career_goal: Optional[str] = Field(
        default=None,
        description="The user's career goal or desired role."
    )

    learning_style: Optional[str] = Field(
        default=None,
        description="The user's preferred learning style."
    )

    preferred_location: Optional[str] = Field(
        default=None,
        description="Preferred job or work location."
    )

    preferred_industry: Optional[str] = Field(
        default=None,
        description="Preferred industry or career field."
    )


memory_llm = llm_groq.with_structured_output(MemorySchema)


# --------------------------------
# Memory Extractor Node
# --------------------------------

def memory_extractor_node(state: GraphState) -> GraphState:

    user_query = state["query"]
    user_id = state.get("user_id", "default_user")

    prompt = f"""
You are a memory extraction assistant.

Extract only stable and useful personal preferences or career-related
facts from the user's message.

User message:
{user_query}

Possible memories:
- career goal
- preferred learning style
- preferred location
- preferred industry

Rules:
- Do not guess.
- If a fact is not explicitly stated, return null.
- Do not store temporary questions or general research topics.
"""

    memory = memory_llm.invoke(prompt)

    if memory.career_goal:
        save_memory(
            user_id,
            "career_goal",
            memory.career_goal
        )

    if memory.learning_style:
        save_memory(
            user_id,
            "learning_style",
            memory.learning_style
        )

    if memory.preferred_location:
        save_memory(
            user_id,
            "preferred_location",
            memory.preferred_location
        )

    if memory.preferred_industry:
        save_memory(
            user_id,
            "preferred_industry",
            memory.preferred_industry
        )

    return state