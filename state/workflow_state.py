from typing import TypedDict, Optional


class WorkflowState(TypedDict, total=False):
    trend: str
    analysis: str
    content: str
    grade: str
