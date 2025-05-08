from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph.workflow import build_workflow
app = FastAPI(
    title="Social Media",
    description="Multi agent workflow for trend analyzing,content generation and content grading.",
    version="1.0.0",
)

workflow = build_workflow()

@app.post("/run")
async def run_workflow():
    try:
        initial_state = {}
        result = workflow.invoke(initial_state)

        return {
                "trend": result.get("trend"),
                "content": result.get("content"),
                "grade": result.get("grade"),
                "approved": result.get("grade", 0) >= 80
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))