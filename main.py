from langchain_core.messages import HumanMessage
from llm import content_grader_model
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
from graph.workflow import build_workflow
from agents.trend_analyzer import get_top_trends_for_query
app = FastAPI(
    title="Social Media",
    description="Multi agent workflow for trend analyzing,content generation and content grading.",
    version="1.0.0",
)

workflow = build_workflow()


class TrendInput(BaseModel):
    query: Optional[str] = None
    selected_trend: Optional[str] = None


@app.post("/run")
async def run_workflow(input_data: TrendInput):
    try:
        if input_data.query and not input_data.selected_trend:
            top_trends = get_top_trends_for_query(input_data.query)
            return {"top_trends": top_trends}
        elif input_data.selected_trend:

            initial_state = {"trend": input_data.selected_trend}
            result = workflow.invoke(initial_state)
            return {
                "trend": result.get("trend"),
                "content": result.get("content"),
                "grade": result.get("grade"),
                "approved": result.get("grade", 0) >= 80,
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
