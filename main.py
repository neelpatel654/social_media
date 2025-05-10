from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
from graph.workflow import build_workflow
from agents.trend_analyzer import get_top_trends
app = FastAPI(
    title="Social Media",
    description="Multi agent workflow for trend analyzing,content generation and content grading.",
    version="1.0.0",
)

workflow = build_workflow()


class TrendInput(BaseModel):
    trend: Optional[str] = None


@app.post("/run")
async def run_workflow(input_data: TrendInput):
    try:
        if not input_data.trend:
            top_trends = get_top_trends()
            return {"top_trends": top_trends}
        else:
            initial_state = {"trend": input_data.trend}
            result = workflow.invoke(initial_state)
            return {
                "trend": result.get("trend"),
                "content": result.get("content"),
                "grade": result.get("grade"),
                "approved": result.get("approved"),
            }
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
