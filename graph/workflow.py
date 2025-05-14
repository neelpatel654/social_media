from langgraph.graph import StateGraph, START, END
from agents import trend_analyzer, content_generator, content_grader
from state.workflow_state import WorkflowState
import os
from dotenv import load_dotenv
from langgraph.types import interrupt
from langgraph.checkpoint.memory import MemorySaver
load_dotenv()

memory = MemorySaver()


def build_workflow():
    graph = StateGraph(WorkflowState)

    # graph.add_node("trend_analyzer", trend_analyzer.analyze_trend)

    # user selection node
    # def user_input(state: dict) -> dict:
    #     print("before<<<<<<<<<---------.>>>>>>>>>>>>>")
    #     interrupt(value="what is your age?")
    #     print("hello<<<<<<<<<---------.>>>>>>>>>>>>>")
    #     return state

    def user_input(state: dict) -> dict:
        print("before<<<<<<<<<---------.>>>>>>>>>>>>>")
        return interrupt(value="wait for user to select trend")

    graph.add_node("user_input", user_input)
    graph.add_node("content_generator", content_generator.generate_content)
    graph.add_node("content_grader", content_grader.grade_content)

    graph.add_edge(START, "user_input")
    graph.add_edge("user_input", "content_generator")
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

    return graph.compile(checkpointer=memory)
