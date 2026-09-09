from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from backend.app.graph.state import GraphState
from backend.app.graph.memory_extractor import memory_extractor_node
from backend.app.graph.orchestrator import orchestrator_node
from backend.app.graph.worker import worker_node
from backend.app.graph.collector import collector_node


# --------------------------------
# Short-Term Memory
# --------------------------------

memory = MemorySaver()


# --------------------------------
# Build LangGraph Workflow
# --------------------------------

def build_graph():

    graph = StateGraph(GraphState)

    graph.add_node(
        "memory_extractor",
        memory_extractor_node
    )

    graph.add_node(
        "orchestrator",
        orchestrator_node
    )

    graph.add_node(
        "worker",
        worker_node
    )

    graph.add_node(
        "collector",
        collector_node
    )

    graph.add_edge(
        START,
        "memory_extractor"
    )

    graph.add_edge(
        "memory_extractor",
        "orchestrator"
    )

    graph.add_edge(
        "orchestrator",
        "worker"
    )

    graph.add_edge(
        "worker",
        "collector"
    )

    graph.add_edge(
        "collector",
        END
    )

    return graph.compile(
        checkpointer=memory
    )


app_graph = build_graph()