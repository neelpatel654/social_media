from functools import partial
from logging import config
from langchain_core.messages import HumanMessage
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
from graph.workflow import build_workflow
from agents.trend_analyzer import get_top_trends_for_query
import uuid
from langgraph.types import Command

app = FastAPI(
    title="Social Media",
    description="Multi agent workflow for trend analyzing,content generation and content grading.",
    version="1.0.0",
)

workflow = build_workflow()


class TrendInput(BaseModel):
    query: Optional[str] = None
    selected_trend: Optional[str] = None
    run_id: Optional[str] = None


session_store = {}


@app.post("/run")
async def run_workflow(input_data: TrendInput):
    try:
        if input_data.query and not input_data.selected_trend:

            run_id = "123"

            top_trends = get_top_trends_for_query(input_data.query)
            print("top trends------------->>>>>>>>>>>>>>>>>>", top_trends)
            partial_state = workflow.invoke(
                input={"query": input_data.query, "trends": top_trends}, config={"run_id": run_id, "thread_id": run_id})

            session_store[run_id] = partial_state
            print("first---------->>>>>")
            return {"run_id": run_id,
                    "top_trends": top_trends,
                    "message": "Select one trend and call again with selected_trend and run_id"}

        elif input_data.selected_trend and input_data.run_id:

            print("before run_id------------->>>>>>>>>>>>>>>>>>", input_data.run_id)
            run_id = input_data.run_id
            print("after run_id------------->>>>>>>>>>>>>>>>>>", run_id)
            paused_state = session_store.get(run_id)
            print("hello---------->>>>>>>>>>>>>")
            if not paused_state:
                raise HTTPException(status_code=400, detail="Invalid run_id")

            final_result = workflow.invoke(
                Command(resume={"trend": input_data.selected_trend}),
                config={"run_id": run_id, "thread_id": run_id}
                # state=paused_state
            )
            print("before delete------------->>>>>>>>>>>>>>>>>>")
            del session_store[run_id]
            print("after delete------------->>>>>>>>>>>>>>>>>>")

            return {
                "trend": final_result.get("trend"),
                "content": final_result.get("content"),
                "grade": final_result.get("grade"),
                "approved": final_result.get("grade", 0) >= 80,
            }
        else:
            raise HTTPException(
                status_code=400, detail="You must have to provide either query or selected trend")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# ===================================================================================
# @app.post("/start")
# async def start_workflow():
#     try:
#         initial_state = {}
#         result = workflow.invoke(initial_state)
#         return {
#             "trends": result.get("trends", [])
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
# class ResumeRequest(BaseModel):
#     trend: str
# @app.post("/run")
# async def run_workflow(request: ResumeRequest):
#     try:
#         state = {"trend": request.trend}
#         result = workflow.invoke(state)
#         return {
#             "trend": result.get("trend"),
#             "content": result.get("content"),
#             "grade": result.get("grade"),
#             "approved": result.get("grade", 0) >= 80
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# system_message = """
#     You are a helpful assistant that extracts the main trend title or topic from a user's query to help identify trending or popular subjects.
# Given a user's query, return only the one word trend title or topic — concise, specific, and suitable for web search or trend analysis """

# human_message = HumanMessage(
#     content=(
#         "user_request: Find me top trending topics related to bollywood movies in india"
#     )
# )

# optimized_response = content_grader_model.invoke(
#     [system_message, human_message])
# optimized_web_request = optimized_response.content
# print("[OPTIMIZE QUERIES] Optimized request:", optimized_web_request)
