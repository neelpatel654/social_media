from langgraph.graph import StateGraph, START, END
from agents import trend_analyzer, content_generator, content_grader
from state.workflow_state import WorkflowState
import os
from dotenv import load_dotenv
load_dotenv()


def build_workflow():
    graph = StateGraph(WorkflowState)

    graph.add_node("trend_analyzer", trend_analyzer.analyze_trend)
    graph.add_node("content_generator", content_generator.generate_content)
    graph.add_node("content_grader", content_grader.grade_content)

    graph.add_edge(START, "trend_analyzer")
    graph.add_edge("trend_analyzer", "content_generator")
    graph.add_edge("content_generator", "content_grader")
    graph.add_conditional_edges(
        "content_grader",
        lambda state: "approve" if state.get(
            "grade", 0) >= 80 else "regenerate",
        {
            "approve": END,
            "regenerate": "content_generator"
        }
    )

    return graph.compile()
