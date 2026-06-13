from langgraph.graph import StateGraph, END

from ai_pipeline.graph.state import GraphState
from ai_pipeline.graph.routing import validation_router

from ai_pipeline.agents.structuring_agent import structuring_agent
from ai_pipeline.agents.validation_agent import validation_agent
from ai_pipeline.agents.repair_agent import repair_agent

def build_workflow():

    graph = StateGraph(GraphState)

    # Nodes
    graph.add_node("structuring", structuring_agent)
    graph.add_node("validation", validation_agent)
    graph.add_node("repair", repair_agent)

    # Entry point
    graph.set_entry_point("structuring")

    # Normal edges
    graph.add_edge("structuring", "validation")
    graph.add_edge("repair", "validation")

    # Conditional routing
    graph.add_conditional_edges(
        "validation",
        validation_router,
        {
            "success": END,
            "repair": "repair",
            "failed": END,
        },
    )

    return graph.compile()


workflow = build_workflow()


