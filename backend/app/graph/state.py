from typing import TypedDict, List


class GraphState(TypedDict):
    query: str
    tasks: List[str]
    results: List[str]
    summary: str

    # Short-term conversation memory
    chat_history: List[dict]

    # Used later for long-term memory
    user_id: str