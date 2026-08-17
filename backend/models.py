from pydantic import BaseModel
from typing import List, Optional

class ReviewComment(BaseModel):
    line: int
    comment: str

class ReviewResult(BaseModel):
    score: int
    recommendation: str
    comments: List[ReviewComment]

class AnalyzeRequest(BaseModel):
    repo_name: str
    pr_number: int
